import os
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher


# Function to read resumes from the folder one by one
# mypath = 'Resumes'  # enter your path here where you saved the resumes
# onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


# def pdfextract(filename):
#     with open(filename, 'rb') as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     # print(text)
#     return text

# function that does phrase matching and builds a candidate profile
def create_profile(text, file_name):
    text = str(text)
    text = text.replace("\\n", "")
    text = text[text.find('SKILLS') + 6: text.find('PROJECTS')]
    text = text.lower()
    # below is the csv where we have all the keywords, you can customize your own
    keyword_dict = pd.read_csv('templete_CVS.csv')
    stats_words = [nlp(text) for text in keyword_dict['Statistics'].dropna(axis=0)]
    NLP_words = [nlp(text) for text in keyword_dict['NLP'].dropna(axis=0)]
    ML_words = [nlp(text) for text in keyword_dict['Machine Learning'].dropna(axis=0)]
    DL_words = [nlp(text) for text in keyword_dict['Deep Learning'].dropna(axis=0)]
    R_words = [nlp(text) for text in keyword_dict['R Language'].dropna(axis=0)]
    python_words = [nlp(text) for text in keyword_dict['Python Language'].dropna(axis=0)]
    Data_Engineering_words = [nlp(text) for text in keyword_dict['Data Engineering'].dropna(axis=0)]
    Developer_Words = [nlp(text) for text in keyword_dict['Developer'].dropna(axis=0)]

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Stats', None, *stats_words)
    matcher.add('NLP', None, *NLP_words)
    matcher.add('ML', None, *ML_words)
    matcher.add('DL', None, *DL_words)
    matcher.add('R', None, *R_words)
    matcher.add('Python', None, *python_words)
    matcher.add('DE', None, *Data_Engineering_words)
    matcher.add('Developer', None, *Developer_Words)
    doc = nlp(text)
    # print(doc)
    d = []
    matches = matcher(doc)
    # print(matches)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start: end]  # get the matched slice of the doc
        d.append((rule_id, span.text))
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())
    # print(keywords)
    # converting string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ', n=1).tolist(), columns=['Subject', 'Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(', n=1).tolist(), columns=['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'], df2['Keyword'], df2['Count']], axis=1)
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    # print(df2)
    # print(df3)
    # base = os.path.basename(file)
    filename = os.path.splitext(file_name)[0]

    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    # print(name2)
    # converting str to dataframe
    name3 = pd.read_csv(StringIO(name2), names=['Candidate Name'])
    # print(name3)
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis=1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace=True)
    # print(dataf)
    return dataf


# function ends

# code to execute/call the above functions


def resume_parser(text, file_name):
    final_database = pd.DataFrame()
    dat = create_profile(text, file_name)
    final_database = final_database._append(dat)

    # code to count words under each category and visulaize it through Matplotlib

    final_database2 = final_database['Keyword'].groupby(
        [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace=True)
    final_database2.fillna(0, inplace=True)
    new_data = final_database2.iloc[:, 1:]
    new_data.index = final_database2['Candidate Name']
    new_data.to_csv('sample.csv')
    print(new_data)
    return new_data

