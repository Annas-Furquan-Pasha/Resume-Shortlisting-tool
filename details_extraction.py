from spacy.matcher import PhraseMatcher
import pandas as pd
import en_core_web_sm
from collections import Counter
import re

nlp = en_core_web_sm.load()

text = '''ANNAS FURQUAN PASHA
7995027220 ⋄Hyderabad, Telangana
annasfurquan27@gmail.com ⋄https://github.com/Annas-Furquan-Pasha
OBJECTIVE
Enthusiastic Flutter and React Developer with a strong passion for creating innovative and user-friendly applications.
A motivated team player with excellent problem-solving skills and a drive to deliver exceptional results.
EDUCATION
M. Tech   
Jawaharlal Nehru Technological University Hyderabad
B.Tech in Computer Science Engineering 2024
•Current CGPA : 8.80
Narayana Junior College, Alwal
MPC- Intermediate 2020
•Percentage : 98.00 (980/1000)
•TS EAMCET Rank : 1073
•JEE MAINS AIR : 18693, OBC-NCL Rank : 4136
Narayana High Schoool, Old Alwal
SSC 2018
•GPA : 9.7
•particitpated in interschool seminar and debate
•Qualified till stage 2 out of 3 in Quiz Competition hosted by Siddharth Basu .
SKILLS
Technical Skills Data Structures, Algorithms, Operating System, Computer Networks, DBMS, OOPS
Development Skills Flutter-Dart, React-JS,
Languages C, C++, Java(basic), Python, HTML, JavaScript, MySQL, PHP
Additional Skills Touch Typing ,Problem Solving , Decision Making, Team Building
PROJECTS
•SHOP APP —— Flutter App.
Build an full stack app which has authentication and database as firebase. This app enables user to buy items
and have many options such as to favorite any product and can also put user’s product in that shop.
•BLOG APP —— Node-JS
Built a blog website where user can posts blogs and can compose, delete and read posts
•CHAT APP —— Flutter App.
Build an full stack app with autentication and backend being firebase, in which different users can join and chat
among themselves, by keeping their chat name and profile photo.
•TEXT CONVERTER —— React App
Developed a website which enable user to convert their input in different form such as Capitalize the text and
make it Uppercase or Lowercase.•MEALS APP —— Flutter App.
Build an app which has different cuisines with different recipes and their ingredients. And the option to mark
favorite their recipes.
•Attendance Using Facial Recognition —— Python
Developed a tool for marking attendance using facial recognition using python and backend being Firebase
INTERNSHIPS
•Full Stack Developer in SiVive
Worked as Full stack web developer and build a website which converts pdf to excel document with backed begin
AWS. It has an input screen which allows user to upload pdf file and the next screen to display the files and to
download the excel file
CERTIFICATIONS
•Appreciation certificate from SiVive for developing their website
•Course completion certificate from Udemy for completing Flutter-dart full course
ACHIEVEMENTS
•solved 100+ questions in Data Structures and Algorithms
•Organised a successful event ’Radium Cricket’ at college during cultural fest 
HOBBIES
•Touch Typing
•playing Cricket, Basket Ball
•playing strategical games online'''
text2 = '''P VAMSHI TEJA
Learner . Team Player
+91 6305099374
vamsitejago@gmail.com
Profile Summary
A
quick learner with a passion for software development;
am eager to kickstart my career and apply
my knowledge in a real-world setting: As a dedicated team player;
am committed to continuous learning
and excited to grow alongside the company in pursuit of mutual success:
Education
M Tech
JAWAHARLAL NEHRU TECHNOLOGICAL UNIVERSITY HYDERABAD
2024
B.Tech in Computer Science and Engineering
CGPA/ AGGREGATE : 8.67
GOVERNMENT INSTITUTE OF ELECTRONICS
2021
Diploma in Computer Science and Engineering
CGPA/ AGGREGATE : 88%
SKILLS
Proficient in programming:
Logical and Structured Thinking:
Active user at Coding and Problem Solving Platforms.
Designer
Languages and Technologies
C, Ctt, JAVA(basic)
HTML, CSS, JAVASCRIPT
SQL, Node js(moderate)
PROJECTS
Chat Application (chat room)
Its a chat application, where different people can join and chat among themselves and the
messages aren't recorded once the session gets terminated:
Built using : HTML, CSS, node js'''
files = [text, text2]
file_names = ['annas', 'vamshi']
def education_extraction(files, file_names):
    data = pd.DataFrame(columns=['Candidate Name', 'Qualification'])
    for z in range(len(files)):
        text = files[z]
        text = text[text.find('EDUCATION') + 9: text.find('SKILLS')]
        text = text.lower()
        keyword_dict = pd.read_csv('education.csv')
        B_Tech = [nlp(text) for text in keyword_dict['B Tech'].dropna(axis=0)]
        M_Tech = [nlp(text) for text in keyword_dict['M Tech'].dropna(axis=0)]
        PHD = [nlp(text) for text in keyword_dict['PHD'].dropna(axis=0)]
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
            data.loc[len(data)] = {'Candidate Name': file_names[z], 'Qualification': 'M Tech'}
        elif 'BTech' in keywords:
            data.loc[len(data)] = {'Candidate Name': file_names[z], 'Qualification': 'B Tech'}
        else:
            data.loc[len(data)] = {'Candidate Name': file_names[z], 'Qualification': 'No Degree'}
    # print(data)
    return data


def get_number(text):
    """
    This function returns a list of a phone number from a list of text
    :param text: list of text
    :return: list of a phone number
    """
    # compile helps us to define a pattern for matching it in the text
    pattern = re.compile(
        r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
    # findall finds the pattern defined in compile
    pt = pattern.findall(text)

    # sub replaces a pattern matching in the text
    pt = [re.sub(r'[,.]', '', ah) for ah in pt if len(re.sub(r'[()\-.,\s+]', '', ah)) > 9]
    pt = [re.sub(r'\D$', '', ah).strip() for ah in pt]
    pt = [ah for ah in pt if len(re.sub(r'\D', '', ah)) <= 15]

    for ah in list(pt):
        # split splits a text
        if len(ah.split('-')) > 3: continue
        for x in ah.split("-"):
            try:
                # isdigit checks whether the text is number or not
                if x.strip()[-4:].isdigit():
                    if int(x.strip()[-4:]) in range(1900, 2100):
                        pt.remove(ah)

            except:
                pass

        number = None
        number = list(set(pt))
        return number

print(education_extraction(files, file_names))