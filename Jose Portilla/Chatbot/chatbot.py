# Building Chatbot with Deep NLP

#Importing Libraries

import numpy as np
import tensorflow as tf
import re
import time

################## PART I - DATA PRE PROCESSING #####################

#Importing Dataset

lines = open('movie_lines.txt',encoding = 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt',encoding = 'utf-8', errors = 'ignore').read().split('\n')

# Creating a dictionary that maps each line and its id
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ') # _line represents a temperory variable 
    if len(_line) == 5:
        id2line[_line[0]]=_line[4]


# Creating a list of all the conversations
conversations_ids =[]        
for conversation in conversations[:-1]: # The last row of the converstaion dataset is empty, hence we are excluding 
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","" ) 
    # we need only the last row hence -1. [1:-1] will exclude the brackets and replacing the single quotes with nothing
    conversations_ids.append(_conversation.split(","))

# Getting seperately the question and the answers
questions =[]
answers =[]
for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
        
# Cleaning the text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm","i am", text)
    text = re.sub(r"he's","he is", text)
    text = re.sub(r"she's","she is", text)
    text = re.sub(r"he's","he is", text)
    text = re.sub(r"that's","that is", text)
    text = re.sub(r"what's","what is", text)
    text = re.sub(r"where's","where is", text)
    text = re.sub(r"\'ll"," will", text)
    text = re.sub(r"\'ve"," have", text)
    text = re.sub(r"\'re"," are", text)
    text = re.sub(r"\'d"," would", text)
    text = re.sub(r"won't","will not", text)
    text = re.sub(r"can't","cannot", text)
    text = re.sub(r"[-()\"#/@:;<>{}+=|.?,]","", text) #-()\"#/@:;<>{}+=|.?, removing these symbols
    return text

# Cleaning the questions 
clean_questions = []    
for question in questions:
    clean_questions.append(clean_text(question))
    
# Cleaning the answers
clean_answers = []    
for answer in questions:
    clean_answers.append(clean_text(answer))

# Creating a dictionary that maps each word to its number of occurences
word2count ={}
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1

# Creating two dictionaries that map the questions words and the answer words to a unique integer
threshold = 20
questionsword2int = {}
word_number = 0
for word,count in word2count.items():
    if count >= threshold:
        questionsword2int[word] = word_number
        word_number +=1
        
answersword2int = {}
word_number = 0
for word,count in word2count.items():
    if count >= threshold:
        answersword2int[word] = word_number
        word_number +=1

# Adding the last tokens to these two dictonaries
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']

for token in tokens:
    questionsword2int[token]= len(questionsword2int)+1
for token in tokens:
    answersword2int[token]= len(answersword2int)+1
    
# creating the inverse dictionary of the answerswords2int dictionary
answersints2word = {w_i: w for w, w_i in answersword2int.items()} # I slightly changed the code here in variable name instead of answerswords2int

# Adding the End of String token to the end of every answer

for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'


# Translating all the questions and the answers into integers
# and Replacing all the words that were filtered out by <OUT>

questions_to_int = []
for question in clean_questions:
    ints = [ ]
    for word in question.split():
        if word not in questionsword2int:
            ints.append(questionsword2int['<OUT>'])
        else:
            ints.append(questionsword2int[word])
    questions_to_int.append(ints)
    
answers_to_int = []
for answer in clean_answers:
    ints = [ ]
    for word in answer.split():
        if word not in answersword2int:
            ints.append(answersword2int['<OUT>'])
        else:
            ints.append(answersword2int[word])
    answers_to_int.append(ints)
    

# sorting questions and answers by the length of questions

sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 25 + 1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])
            
###############  PART 2 - BUILDING THE SEQ2SEQ MODEL ################################
            
# Creating Placeholders for the inputs and the targets

def model_inputs():
    inputs = tf.placeholders(tf.int32,[None,None],name = 'input')
    targets = tf.placeholders(tf.int32,[None,None],name = 'target')
    lr = tf.placeholders(tf.float32,name = 'learning_rate')
    keep_prob = tf.placeholders(tf.float32,name = 'keep_prob') #This controls the dropouts
    return inputs,targets,lr,keep_prob


# Preprocessing the targets. This is required because targets acccepts specific format
    


    














    
    
    
    
    
    
    
    
    
    
    
    
    
    