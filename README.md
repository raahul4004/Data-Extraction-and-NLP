
# Data-Extraction-and-NLP

This repository contains Python scripts for data extraction and Natural Language Processing (NLP) analysis. The primary goal is to extract data from URLs and perform NLP analysis on the text data.

## Instructions

1. The two main Python files in this repository are:
   - `data_extraction.py`: Used for extracting data from URLs and saving it to text files.
   - `data_analysis.py`: Performs NLP analysis on the extracted text data and saves the analysis to an Excel file.

2. To get started, execute `data_extraction.py` first. This script will read URLs from the `Input.xlsx` file and write the title and content of the web pages to text files. The extracted data will be stored in the "Data_Extracted_from_Websites_to_text_files" folder.

3. Libraries required for data extraction:
   - BeautifulSoup
   - Requests
   - Pandas

4. After extracting the data, execute `data_analysis.py`. This script performs various NLP analyses on the text documents and writes the results to an Excel file named "Output.xlsx."

5. Modules required for data analysis:
   - Pandas
   - nltk
   - re
   - string

6. All the data extracted from websites is saved in the "Data_Extracted_from_Websites_to_text_files" folder.

7. The NLP analysis includes the following metrics:
   - Sentiment analysis: Positive score, negative score, and polarity.
   - Subjectivity Score.
   - Analysis of Readability: Fog index.
   - Average Number of Words Per Sentence.
   - Complex Word Count.
   - Word Count.
   - Syllable Count Per Word.
   - Personal Pronouns.
   - Average Word Length.

## Usage

Follow these steps to use the repository:

1. Clone the repository to your local machine.

2. Ensure you have the required libraries and modules installed for both data extraction and analysis.

3. Place the URLs you want to analyze in the "Input.xlsx" file.

4. Run `data_extraction.py` to extract the data.

5. Run `data_analysis.py` to perform NLP analysis and generate the "Output.xlsx" file with the results.

##
For any questions or issues, please contact me at raahul4004@gmail.com
