from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from app.auth import authentication
from .process import *
from .models import *
import pickle
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Import Model
# Load the saved model
model = pickle.load(open('dataset/marks_prediction.pkl', 'rb'))
vectorizer = pickle.load(open('dataset/subjective_analysis_vector.pkl', 'rb'))
# Create your views here.

def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            questions, marks = select_questions()
            qus = questions_random(question = questions, marks = marks)
            qus.save()
            messages.success(request, "Log In Successful...!")
            return HttpResponseRedirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
            # return HttpResponse("This is Home page")
    return render(request, "register.html")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    questions = questions_random.objects.last()
    qus = eval(questions.question)
    original_marks = eval(questions.marks)
    context = {
        'fname': request.user.first_name, 
        'questions' : qus,
        'original_marks' : original_marks,
        }
    if request.method == 'POST':
        # Process the form data
        try:
            answers = []
            for key, value in request.FILES.items():
                if key.startswith('answer'):
                    answers.append(value)

            diagrams = []
            for key, value in request.FILES.items():
                if key.startswith('diagram'):
                    diagrams.append(value)
            # Extract text from each uploaded image
            extracted_texts = []
            for answer_file in answers:
                if isinstance(answer_file, UploadedFile):
                    # Open the uploaded image file
                    image = Image.open(answer_file)
                    # Extract text using Tesseract OCR
                    text = pytesseract.image_to_string(image)
                    extracted_texts.append(text.strip())

            # Create a dictionary mapping questions to extracted answers
            question_answer_dict = {q: a for q, a in zip(qus, extracted_texts)}
            question_diagram_dict = dict(zip(qus, diagrams))
            dataset_path = 'dataset/dataset.csv'
            df = pd.read_csv(dataset_path)
            # Create a dictionary mapping questions to original diagram paths
            question_original_diagram_dict = pd.Series(df.Diagram.values, index=df.Question).to_dict()
            print(question_original_diagram_dict)
            marks_on_diagrams = check_diagrams(question_diagram_dict, question_original_diagram_dict)
            print("MArks : ",marks_on_diagrams)
            marks_partial = check_answers(question_answer_dict)
            
            final_marks =[]
            final_result = []

            for mark in marks_partial:
                if mark == 0:
                    final_marks.append(0)
                else:
                    len_marks = len(mark)
                    predicted_marks = model.predict([[len_marks]])
                    predicted_marks = predicted_marks[0]
                    predicted_marks = int(predicted_marks)
                    final_marks.append(predicted_marks)

            for i, similarity_score in enumerate(marks_on_diagrams):
                # Check if the similarity score is greater than 0.80
                if similarity_score > 0.80:
                    # Add 2 to the corresponding final mark
                    final_marks[i] += 2
                    # Ensure the final mark does not exceed the original mark
                    if final_marks[i] > original_marks[i]:
                        final_marks[i] = original_marks[i]

            # Output the updated final marks
            print("Updated Final Marks:", final_marks)
            
            for question, answer in question_answer_dict.items():
                # Find the index of the current question in the dictionary
                index = list(question_answer_dict.keys()).index(question)
                
                # Create a new list with the question, answer, original marks, and predicted marks
                row = [question, answer, original_marks[index], final_marks[index]]
                
                # Append the row to the output list
                final_result.append(row)
            print("Final Result : ",final_result)
            pred = predicted_results(ques_ans = question_answer_dict, marks = final_marks, final_result = final_result)
            pred.save()
            return redirect('results')
        except:
            messages.error(request, "Something wents Wrong with Test, Please Restart your Test!!!")
            return redirect('log_out')
    return render(request, "dashboard.html",context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def results(request):
    pred = predicted_results.objects.last()
    ques_ans = eval(pred.ques_ans)
    marks = eval(pred.marks)
    final_result = eval(pred.final_result)
    context = {
        'fname': request.user.first_name,
        'ques_ans': ques_ans,
        'marks': marks,
        'final_result': final_result
    }
    return render(request, 'results.html', context)