import PyPDF2
import pandas as pd
import streamlit as st

from app import resume_parser
from plot import plot
from education_extraction import education_extraction_text

def app():
    st.title('Resume Shortlisting Tool')
    st.write('INSTRUCTIONS FOR PDF FORMAT')
    st.write('- Name of the pdf file should be candidate name')
    st.write('- Resume should be in simple format(chronological)')
    st.write('- Follow this pattern ')
    st.write('Name > objective/summery/overview/profile > Education > Skills > Projects')
    st.write('- All above mentioned headings should be in capital letters')
    upload_file = st.file_uploader('Upload Resume', type=['pdf'])
    text = ""
    if upload_file is not None:
        pdf_reader = PyPDF2.PdfReader(upload_file)
        for page in pdf_reader.pages:
            text += page.extract_text()

        data = resume_parser(text, upload_file.name)
        plot(data, upload_file.name)
        st.write(data)
        st.write(f'Highest Qualification : {education_extraction_text(text)}')
        st.image(f'plots/{upload_file.name}.png')


app()
