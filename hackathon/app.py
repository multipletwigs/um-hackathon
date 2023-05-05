import streamlit as st 
import torch as torch
from st_aggrid import AgGrid
import pandas as pd
import io
import asyncio 
import pandas as pd
from parser import *

def introduction():
    st.title("Please input a PDF Folder")

async def upload_form():
    # Streamlit input fields 
    uploaded_files = st.file_uploader('Upload pitch decks here',
    accept_multiple_files=True, type="pdf")
    parsed_pdfs = []

    clicked = st.button(label="Parse Pitch Decks!") 
    if clicked:
        if len(uploaded_files) == 0:
            # Show error banner that there are no files 
            st.error("Please upload a PDF pitch deck") 
        else:
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.getvalue()
                parser = Parser(io.BytesIO(file_bytes)) 
                # show loading state 
                with st.spinner("Parsing PDF..."):
                    json_response = await parser.get_criterias() 
                    json_df = parser.json_to_df(json_response)
                    parsed_pdfs.append(json_df) 

    return parsed_pdfs

def display_parsed_pdfs(parsed_pdfs):
    # Display the parsed pdfs
    df = None 
    for parsed_pdf in parsed_pdfs:
        if df is None:
            df = pd.DataFrame(parsed_pdf)
        else:
            df = df.append(parsed_pdf, ignore_index=True)

    if df is not None:
        st.table(df.transpose())

if __name__ == "__main__":
    introduction() 
    parsed_pdfs = asyncio.run(upload_form())
    display_parsed_pdfs(parsed_pdfs)
