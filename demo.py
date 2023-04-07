import streamlit as st 

def generate_heading(title):
    return st.title(title)

if __name__ == "__main__":
    generate_heading("Hello World")