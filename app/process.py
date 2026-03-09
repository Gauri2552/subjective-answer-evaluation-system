import pandas as pd
import random
import csv
import pandas as pd
import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf
import numpy as np
import json
import re
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image

# Load the Universal Sentence Encoder
use_model = hub.load("https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/multilingual/2")

# Load the dataset



def clean_text(text):
    # Remove non-alphanumeric characters and symbols
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

def accuracy(expected_answer, answer):
    expected_answer = clean_text(expected_answer)
    answer = clean_text(answer)
    embedding1 = use_model([expected_answer])[0]
    embedding2 = use_model([answer])[0]
    match_avg = round(((cosine_similarity(embedding1, embedding2)) * 100) , 2)
    return match_avg

# Read the CSV file
df = pd.read_csv('dataset/dataset.csv')

def select_questions():
    # Select a random sample of 10 rows from the DataFrame
    sample_df = df.sample(n=10)

    # Get the questions from the 'Question' column of the sample DataFrame
    questions = sample_df['Question'].tolist()
    marks = sample_df['Marks'].tolist()
    return questions, marks

def check_answers(question_answer_dict):
    # Initialize an empty dictionary
    data_dict = {}
    marks_partial = []
    # Open the CSV file and read its contents
    with open('dataset/dataset.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            question = row['Question']
            answer = row['Answer']
            
            # Store the question and its respective answer in the dictionary
            data_dict[question] = answer
    
    for question, answer in question_answer_dict.items():
        if question in data_dict:
            expected_answer = data_dict[question]
            match_avg = accuracy(expected_answer, answer)
            if match_avg > 50 :
                marks_partial.append(answer)
            else:
                marks_partial.append(0)
    
    return marks_partial

def check_diagrams(question_diagram_dict, question_original_diagram_dict):
    marks_on_diagrams = []
    for question, student_diagram in question_diagram_dict.items():
        if student_diagram:
            # Retrieve the path to the original diagram
            original_diagram_path = question_original_diagram_dict.get(question)
            print(original_diagram_path)
            if original_diagram_path:
                # Load the original and student's diagrams
                original = cv2.imread(original_diagram_path, cv2.IMREAD_GRAYSCALE)
                student_image = Image.open(student_diagram)
                student_image = np.array(student_image.convert('L'))  # Convert to grayscale

                # Check if images are loaded properly
                if original is None:
                    raise FileNotFoundError(f"Original diagram not found: {original_diagram_path}")
                if student_image is None:
                    raise ValueError(f"Student's diagram for question '{question}' is invalid.")

                # Resize student's diagram to match the original diagram size
                student_image = cv2.resize(student_image, (original.shape[1], original.shape[0]))

                # Compute Structural Similarity Index (SSIM)
                similarity_index, diff = ssim(original, student_image, full=True)
                marks_on_diagrams.append(similarity_index)
            else:
                raise ValueError(f"No original diagram found for question '{question}'.")
        else:
            marks_on_diagrams.append(0)  # No diagram provided by the student
    return marks_on_diagrams