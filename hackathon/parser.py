import pypdf 
from PyPDF2 import PdfReader
import os 
import openai
import json
import streamlit as st
import pandas as pd
import dbaccess
import traceback
from fpdf import FPDF
import aspose.words as aw

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
      json_format[splits[0].strip()] = splits[1]
      
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
          problem=json_format["Problem Statement"],
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
        traceback.print_exc()
        print(f"Error: {e}")
      
    else:
      # just get from db
      
      row_data = row.data[0]
      
      return {
          "Product Name": row_data["pitch_product"],
          "Category": row_data["pitch_category"],
          "Problem Statement": row_data["pitch_problem"],
          "Solution": row_data["pitch_solution"],
          "Business Model": row_data["pitch_business_model"],
          "Market Analysis": row_data["pitch_market_analysis"],
          "Team": row_data["pitch_team"]
        }

  def investment_memo(self, vc_company, json_response):
    try:
      openai.api_key = os.environ['OPENAI_API']
      body = {
        "role": "user",
        "content": f"Generate an investment memo that is from {vc_company} for this this company based on the given information \n\n{json.dumps(json_response)}" 
      }
      
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[body])
      content = response.choices[0].message.content
      
      doc = aw.Document()      
      builder = aw.DocumentBuilder(doc)

      builder.writeln(content)
      
      doc.save("test.pdf")
      
      
    except:
      traceback.print_exc()
      
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

  parser.investment_memo("Ignite Asia", json.dumps({'id': 6, 'created_at': '2023-05-06T07:48:14.939942+00:00', 'pitch_problem': " Price is a concern for customers booking travel online and hotels don't offer a local connection to the city. There is no easy way to book a room with a local or become a host. ", 'pitch_solution': ' AirBed & Breakfast is a web platform where users can rent out their space to host travelers, providing a way to save money when traveling, make money when hosting and share the local culture. ', 'pitch_business_model': ' AirBed & Breakfast takes a 10% commission on each transaction. ', 'pitch_market_analysis': ' There were over 46,000 listings on temporary housing site couchsurfing.com and 17,000 temporary housing listings on SF & NYC Craigslist in the time period of 07/09 to 07/16. The available market size was valued at $51.9 billion, with a serviceable market of 10.6 million trips. ', 'pitch_market_size': 'N/A', 'pitch_team': ' No information provided.', 'pitch_competitive_landscape': 'N/A', 'pitch_competitive_advantage': 'N/A', 'pitch_category': ' Travel/ Accommodation ', 'pitch_filehash': 'c291ca07570a81536e5aec09b61877b38414dd8ee7fbe3ea11c010a1032513ce', 'pitch_product': ' AirBed & Breakfast '}))
