import PyPDF2
import streamlit as st

from app import resume_parser
from plot import plot
from details_extraction import get_details


def main():
    st.title('Resume Shortlisting Tool')
    st.write('INSTRUCTIONS FOR PDF FORMAT')
    st.write('- Name of the pdf file should be candidate name')
    st.write('- Resume should be in simple format(chronological)')
    st.write('- Follow this pattern ')
    st.write('Name > objective/summery/overview/profile > Education > Skills > Projects')
    st.write('- All above mentioned headings should be in capital letters')
    upload_file = st.file_uploader('Upload Resume', type=['pdf'], accept_multiple_files=True)
    if upload_file is not None:
        only_files = []
        file_names = []

        for file in upload_file:
            text = ''
            file_names.append(file.name)
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
            only_files.append(text)

        data = resume_parser(only_files, file_names)
        if data is not None:
            plot(data)
            # st.write(data)
            st.write('Details')
            st.write(get_details(only_files, file_names))
            st.image(f'plots/new_plot.png')


main()

# pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
