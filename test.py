dict1 = {'question1': 'Answer1', 'question2': 'Answer2'}
original_marks = [2, 4]
predicted_marks = [1, 3]

output = []
for question, answer in dict1.items():
    # Find the index of the current question in the dictionary
    index = list(dict1.keys()).index(question)
    
    # Create a new list with the question, answer, original marks, and predicted marks
    row = [question, answer, original_marks[index], predicted_marks[index]]
    
    # Append the row to the output list
    output.append(row)

print(output)
