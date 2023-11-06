#importing all required libraries for data analysis
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import nltk
from nltk import word_tokenize
import syllables
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize
import string
url_dataset = pd.read_excel('Input.xlsx')
url_ids = url_dataset['URL_ID']



#Function to convert list to string
def listToString(s):
 
    # initialize an empty string
    str1 = " "
 
    # return string
    return (str1.join(s))


#Making a string containing all stop words from the StopWords folder 
with open('StopWords\StopWords_Auditor.txt', encoding = 'utf-8') as f1:
    stop_words = f1.read()

with open('StopWords\StopWords_Currencies.txt', encoding = "ISO-8859-1") as f2:
    stop_words += f2.read()

with open('StopWords\StopWords_DatesandNumbers.txt', encoding = "utf-8") as f3:
    stop_words += f3.read()

with open('StopWords\StopWords_Generic.txt', encoding = "utf-8") as f4:
    stop_words += f4.read()

with open('StopWords\StopWords_GenericLong.txt', encoding = "utf-8") as f5:
    stop_words += f5.read()

with open('StopWords\StopWords_Geographic.txt', encoding = "utf-8") as f6:
    stop_words += f6.read()

with open('StopWords\StopWords_Names.txt', encoding = "utf-8") as f7:
    stop_words += f7.read()
stop_words = word_tokenize(stop_words.lower())


#Adding all the textual data to list, each element contains text from one url
textual_data_uncleaned = []
for i in url_ids:
    with open(f'{i}.txt',encoding = 'utf-8') as file:
        textual_data_uncleaned.append(file.read())

#Cleaning the textual data by Removing all stop words from the textual data\
textual_data_cleaned = []

for idx, text in enumerate(textual_data_uncleaned):
    text_list = text.split() #Converting the text into list of words
    for word in text_list:
        if word.lower() in stop_words:
            text_list.remove(word) #If word is present in the list of stop_words then removing it from the list
            
    textual_data_cleaned.append(listToString(text_list)) #assigning the text list as string to textual data after removing stop words




#Storing all the positive words from the given positive words dictionary in string
with open('MasterDictionary\positive-words.txt', encoding = 'utf-8') as file1:
    positive_words = file1.read().lower() #Getting all the positive words given in the master dictionary
positive_words = word_tokenize(positive_words)

for word in positive_words:
    if word in stop_words:
        positive_words.remove(word) #If a positive word is found in stop words then removing it from the list of positive words

#Storing all the  words negative from the given negative words dictionary in string
with open(r'MasterDictionary\negative-words.txt', encoding = "ISO-8859-1") as file2:
    negative_words = file2.read().lower() #Getting all the negative words given in the master dictionary
negative_words = word_tokenize(negative_words) #Converting it into a list
for word in negative_words:
    if word in stop_words:
        negative_words.remove(word) #If a positive word is found in stop words then removing it from the list of negative words



tofind = ['Postive_Score','Negative_Score','Polarity_Score','Subjectivity_Score','Avg_Sentence_length','Percentage_Of_Complex_words','Fog_index','Average_number_of_words_per_sentence','Complex_word_count','Word_count','Syllable_per_word','personal_pronouns','Average_word_length']
for column in tofind:
    url_dataset[column] = [0]*len(url_dataset)



# Define a set of stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Function to clean and count words
def count_cleaned_words(text):
    words = nltk.word_tokenize(text)
    cleaned_words = [word.lower() for word in words if word.lower() not in stop_words and word.lower() not in punctuation]
    return len(cleaned_words)



## Main Data Analysis ####

for idx, text in enumerate(textual_data_cleaned):

    #Counting positive words in a string
    positive_count = 0

    #Counting negative words in a string
    negative_count = 0

    #Counting the number of words present
    word_count_cleaned = 0

    


    for word in word_tokenize(text):
        word_count_cleaned = len(text.split())
        if word.lower() in positive_words :
            positive_count += 1

        elif word.lower() in negative_words:
            negative_count += 1


    
    ######## CALCULATIONS ###########
    
    #The final positive word count of text will be the positive score
    positive_score = positive_count

    #The final negative word count of text will be the negative score
    negative_score = negative_count

    #Calculating the polarity score using this formula: Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
    polarity_score = (positive_count - negative_count)/((positive_count+ negative_count) + 0.000001)

    #Calculating the subjectivity Score using this formula: Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
    subjectivity_score = (positive_score + negative_score)/ ((word_count_cleaned) + 0.000001)


    ######## ADDING TO THE DATAFRAME ###########

    #Adding the positive score to the corresponding row and column of the dataframe
    url_dataset.iloc[idx,2] = positive_score

    #Adding the negative score to the corresponding row and column of the dataframe
    url_dataset.iloc[idx,3] = negative_score

    #Adding the polarity score to the corresponding row and column of the dataframe
    url_dataset.iloc[idx,4] = polarity_score

    #Adding the subjectivity score to the corresponding row and column of the dataframe
    url_dataset.iloc[idx,5] = subjectivity_score

 

############################################################
for idx, text in enumerate(textual_data_uncleaned):

    

    #Counting the number of syllables
    syllable_count = 0

    #Counting the number of words present in the unclean
    word_count_uncleaned = 0

    #Storing all sentences in a list using nltk library method "sent_tokenize"
    sentences = sent_tokenize(text)

    #Sentence count will be the number of items in the sentences list
    sentence_count = len(sentences)

    #Complex word count
    complex_count = 0 

    #Counting the characters
    character_count = 0

    #Counting personal pronouns
    personal_pronouns = 0

    #proper word count
    word_count = count_cleaned_words(text)
    
    
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    personal_pronouns = len(pronounRegex.findall(text))

    for word in text.split():

        syllable_count_for_complex_words = 0 
        word_count_uncleaned = len(text.split())      

        # if re.findall("^[I|we|my|ours|us|]", word):
        #     personal_pronouns += 1
        

        if not re.findall(r'^[a-z]+["es."|"ed."|"es?"|"ed?"|"es!"|"ed!"]$', word.lower()):
            for letter in word:
                if letter.isalpha():
                    character_count += 1 #Incrementing the count of a character when a alphabet is found
                if letter in ['a','e','i','o','u','y']:
                    syllable_count += 1
                    syllable_count_for_complex_words += 1
        else:
            for i in range(len(word) - 2):
                if word[i] in ['a','e','i','o','u','y']:
                    syllable_count += 1
                    syllable_count_for_complex_words += 1
            
            for i in range(len(word)):
                if word[i].isalpha():
                    character_count += 1 #Incrementing the count of a character when a alphabet is found
                
        if syllable_count_for_complex_words > 2:
            complex_count += 1

    
    
    #Calculating the average sentence length using:(the number of words / the number of sentences)
    avg_len_sentence = 0
    if sentence_count != 0:
        avg_len_sentence = word_count_uncleaned/sentence_count

    
    ######## CALCULATIONS ###########

    #Calculating the Percentage of complex words using this formula:(the number of complex words / the number of words )*100
    if word_count_uncleaned != 0:
        percentage_of_complex_words = (complex_count * 100 / word_count_uncleaned )
    

    #Calculating the fog index using this formula: 0.4 * (Average Sentence Length + Percentage of Complex words)
    fog_index = 0.4 * (avg_len_sentence + percentage_of_complex_words)

    #Calculating the average words per sentence using this formula : the total number of words / the total number of sentences
    average_words_per_sentence = 0
    if sentence_count != 0:
        average_words_per_sentence = word_count_uncleaned/sentence_count

    #Calculating the average syllables per word using this formula : the total number of words / the total number of sentences
    average_syllable_per_word = 0
    if word_count_uncleaned != 0:
        average_syllable_per_word = syllable_count/word_count_uncleaned


    #Calculating the average length word using this formula : the total number of letters/totol number of words
    average_word_length = 0
    if word_count_uncleaned != 0:
        average_word_length = character_count/word_count_uncleaned



    ######## ADDING TO THE DATAFRAME ###########

    #Adding the average length of a sentence to the corresonding row  and in the dataframe 
    url_dataset.iloc[idx,6] = avg_len_sentence

    #Adding the percentage of complex words count to the corresponding row  and in the dataframe 
    url_dataset.iloc[idx,7] = percentage_of_complex_words

    #Adding the fog index to the corresponding row in the dataframe
    url_dataset.iloc[idx,8] = fog_index

    #Adding the average words per sentence to the corresponding row in the dataframe 
    url_dataset.iloc[idx,9] = average_words_per_sentence

    #Adding the complex words cound to the corresponding row and in the dataframe 
    url_dataset.iloc[idx,10] = complex_count

    #Adding the word count to the corresponding row and in the dataframe
    url_dataset.iloc[idx,11] = word_count

    #Adding the average syllables per word to the corresponding row and in the dataframe
    url_dataset.iloc[idx,12] = average_syllable_per_word

    #Adding the personal pronouns count to the corresponding row and in the dataframe
    url_dataset.iloc[idx,13] = personal_pronouns

    #Adding the average length of word to the corresponding row and in the dataframe
    url_dataset.iloc[idx,14] = average_word_length



#Writing/ Extracting the whole output dataframe to excel 
url_dataset.to_excel('Output.xlsx', index = False, header=['URL_ID','URL','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH'])



    
            


