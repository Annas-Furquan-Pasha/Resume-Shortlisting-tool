import PyPDF2
import streamlit as st

from app import resume_parser
from plot import plot
from details_extraction import education_extraction


def main():
    st.title('Resume Shortlisting Tool')
    st.write('INSTRUCTIONS FOR PDF FORMAT')
    st.write('- Name of the pdf file should be candidate name')
    st.write('- Resume should be in simple format(chronological)')
    st.write('- Follow this pattern ')
    st.write('Name > objective/summery/overview/profile > Education > Skills > Projects')
    st.write('- All above mentioned headings should be in capital letters')
    upload_file = st.file_uploader('Upload Resume', type=['pdf'], accept_multiple_files=True)
    text = ""
    if upload_file is not None:
        only_files = []
        file_names = []

        for file in upload_file:
            file_names.append(file.name)
            # parsing_pdf(file)
            only_files.append(text)
        data = resume_parser(only_files, file_names)
        if data is not None:
            print(only_files[1])
            plot(data)
            st.write(data)
            st.image(f'plots/new_plot.png')
            st.write(education_extraction(only_files, file_names))


main()


# pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 text += page.extract_text()