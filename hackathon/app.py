import streamlit as st 
import torch as torch
from st_aggrid import AgGrid
import pandas as pd
import io
import asyncio 

from parser import Parser
from st_aggrid import AgGrid


def introduction():
    st.title("Upload PDF Pitch Decks")

async def parse_pdf(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    parser = Parser(io.BytesIO(file_bytes))
    with st.spinner("Parsing PDF..."):
        json_response = await parser.get_criterias()
        return parser.json_to_df(json_response)

async def upload_form():
    # Streamlit input fields 
    uploaded_files = st.file_uploader('Upload pitch decks here',
    accept_multiple_files=True, type="pdf")
    temp = None 

    if not uploaded_files:
        st.warning("Please upload one or more PDF pitch decks")
        return

    # if submit button is clicked 
    if st.button("Submit"):
        # Parse the pdfs in async 
        parsed_pdfs = await asyncio.gather(*[parse_pdf(file) for file in uploaded_files])
        temp = parsed_pdfs 
        return pd.concat(parsed_pdfs, ignore_index=True)

def display_parsed_pdfs(df):
    if df is not None:
        st.table(df)

def dropdown_pdf(parsed_pdfs):
    # Create a dropdown for the pdfs
    pdfs = [f"PDF {parsed_pdfs[i]['Product Name']}" for i in range(0, len(parsed_pdfs))]
    pdf = st.selectbox("Select a PDF", pdfs)
    return pdf

def generate_memo(pdf):
    text = ""
    # Generate a memo based on the selected pdf
    st.header("Memo")
    st.text(body=f"Based on the selected PDF, the following is a memo of the pitch deck.")
    st.text(body=f"PDF: {pdf}")
    
    generator = memo.MemoGenerator()

    if st.button("Generate Memo"):
        memo = generator.generate_memo(pdf) 
        for char in memo:
            text += char
            st.text(body=text)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    introduction() 
    parsed_pdfs = asyncio.run(upload_form())
    if 'parsed_pdfs' not in st.session_state and parsed_pdfs is not None:
        st.session_state['parsed_pdfs'] = parsed_pdfs 
    display_parsed_pdfs(st.session_state.get('parsed_pdfs'))

    # Export the parsed pdfs to csv for download
    if 'parsed_pdfs' in st.session_state:
        st.download_button("Download CSV", data=st.session_state.get('parsed_pdfs').to_csv(), file_name="parsed_pdfs.csv", mime="text/csv")
        