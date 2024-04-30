import PyPDF2
from spacy.matcher import PhraseMatcher
import pandas as pd
import en_core_web_sm
from collections import Counter

nlp = en_core_web_sm.load()


def education_extraction_text(text):
    text = text[text.find('EDUCATION')+9 : text.find('SKILLS')]
    text = text.lower()
    keyword_dict = pd.read_csv('education.csv')
    B_Tech = [nlp(text) for text in keyword_dict['B Tech'].dropna(axis=0)]
    M_Tech = [nlp(text) for text in keyword_dict['M Tech'].dropna(axis=0)]
    PHD = [nlp(text) for text in keyword_dict['PHD'].dropna(axis=0)]
    # print(B_Tech)
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('BTech', None, *B_Tech)
    matcher.add('MTech', None, *M_Tech)
    matcher.add('PHD', None, *PHD)

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
    print(keywords)
    if 'MTech' in keywords:
        return 'M Tech'
    elif 'BTech' in keywords:
        return 'B Tech'
    else:
        return 'No Degree'
