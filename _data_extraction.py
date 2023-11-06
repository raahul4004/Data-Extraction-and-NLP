from bs4 import BeautifulSoup
import requests
import pandas as pd

#reading the excel file(containing url_id and urls) as a dataframe using pandas 
url_dataset = pd.read_excel('Input.xlsx')    


#iterating through the url_data set 
for i in  range(len(url_dataset)):

    #getting the html code from the url 
    soup = BeautifulSoup(requests.get(url_dataset.iloc[i,1]).text, 'lxml')
    URL_text = " "

    #Extracting the text from the article tag from the html code. This contains the title and the paragraphs
    if soup.article != None:
        URL_text = f"{soup.title.string} \n "
        for j in soup.article.find_all('p'):
           URL_text += j.text
    
    #creating text files using the title as url_id and the content will be the URL_text
    with open(f"Data_Extracted_from_Websites_to_text_files/{url_dataset.iloc[i,0]}.txt","w", encoding = 'utf-8') as file:
        file.write(URL_text)
    





    
