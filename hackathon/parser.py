import pypdf 
from PyPDF2 import PdfReader
import os 
import openai
import json
import streamlit as st
import pandas as pd
import dbaccess

class Parser: 
  
  def __init__(self, filebytes): 
    self.file_bytes = filebytes
    self.OPENAI_API = os.environ['OPENAI_API'] if os.environ['OPENAI_API'] else st.secrets['OPENAI_API']

  def _parse(self):
    # Parse all text content from the pdf file by page
    pdf = PdfReader(self.file_bytes)
    content = []
    for page in pdf.pages:
      content.append([page.extract_text()])
    return content
  
  def _parse_to_json(self, text):
    # Split by newline 
    strs = text.split("\n") 

    # For each string, split by colon
    json_format = {}
    for s in strs:
      splits = s.split("|")
      json_format[splits[0]] = splits[1]

    return json_format

  async def get_criterias(self):
    filehash = dbaccess.hash_file_bytes(self.file_bytes)
    row = dbaccess.get_row_by_hash(filehash)
    
    if len(row.data) == 0:
      # not in db, process file
      
      # Based on the text content, extract the criterias if any based on open ai
      content = self._parse() 
      criterias = ["Product Name", "Category", "Problem Statement", "Solution", "Business Model", "Market Analysis", "Team"]

      # Compile the content based on criteria with open ai 
      try:
        openai.api_key = os.environ['OPENAI_API']
        body = {
          "role": "user",
          "content": f"Generate a summary of the pitch deck document based on the following criterias: {criterias}. The content of the document is as follows: {content}. \nPlease generate the text in the following format. <Criteria> | <Summary> \n" 
        }

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[body])
        json_format = self._parse_to_json(response.choices[0].message.content)
        
        dbaccess.insert_table(
          problem=json_format["Product Name"],
          solution=json_format["Solution"],
          business_model=json_format["Business Model"],
          market_analysis=json_format["Market Analysis"],
          market_size="N/A",
          team=json_format["Team"],
          competitive_landscape="N/A",
          competitive_advantage="N/A",
          category=json_format["Category"],
          filehash=filehash,
          product=json_format["Product Name"]
        )

        # Parse the response to a json format
        return json_format 

      except Exception as e:
        print(f"Error: {e}")
      
    else:
      # just get from db
      
      row_data = row.data[0]
      
      return json.dumps(
        {
          "Product Name": row_data["pitch_product"],
          "Category": row_data["pitch_category"],
          "Problem Statement": row_data["pitch_problem"],
          "Solution": row_data["pitch_solution"],
          "Business Model": row_data["pitch_business_model"],
          "Market Analysis": row_data["pitch_market_analysis"],
          "Team": row_data["pitch_team"]
        },
        indent=4
      )
      
  def json_to_df(self, json_response):
    # Parse the json response to a dataframe
    # Get keys from json response
    keys = json_response.keys() 
    
    # Extract values from json response
    values = []
    for key in keys:
      values.append(json_response[key])

    # Create a dataframe from the keys and values, where the keys are columns
    df = pd.DataFrame(values, index=keys).transpose()
    return df
      
if __name__ == "__main__":
  parser = Parser("hackathon/pitch_decks/youtube pitch deck (1).pdf")
  parser._parse()
  # parser.get_criterias()




