import streamlit as st 
import pandas as pd
import io
import asyncio 
from parser import Parser
from st_aggrid import AgGrid

def introduction():
    st.title("Upload PDF Pitch Decks")

async def parse_pdf(uploaded_file):
    print(uploaded_file)
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
        # Parse the pdfs
        parsed_pdfs = await asyncio.gather(*[parse_pdf(file) for file in uploaded_files])
        temp = parsed_pdfs 
        return pd.concat(parsed_pdfs, ignore_index=True)

    if temp is not None:
        return pd.concat(temp, ignore_index=True)

def display_parsed_pdfs(df):
    if df is not None:
        st.table(df)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    introduction() 
    parsed_pdfs = asyncio.run(upload_form())
    if parsed_pdfs is not None:
        display_parsed_pdfs(parsed_pdfs)