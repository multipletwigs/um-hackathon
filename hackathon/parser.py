import pypdf 
from PyPDF2 import PdfReader
import os 
import openai
import environments 
import json
import pandas as pd

class Parser: 
  
  def __init__(self, filebytes): 
    self.file_bytes = filebytes

  def _parse(self):
    # Parse all text content from the pdf file by page
    pdf = PdfReader(self.file_bytes)
    content = []
    for page in pdf.pages:
      print(page)
      content.append([page.extract_text()])
    print(content)
    return content

  async def get_criterias(self):

    # Based on the text content, extract the criterias if any based on open ai
    content = self._parse() 
    criterias = ["Product Name", "Category", "Problem Statement", "Solution", "Business Model", "Market Analysis", "Team"]

    # Compile the content based on criteria with open ai 
    try:
      openai.api_key = os.environ['OPENAI_API']
      body = {
        "role": "user",
        "content": f"Generate a summary of the document based on the following criterias: {criterias}. The content of the document is as follows: {content}. \nPlease generate the text in JSON format where the property names are in double quotes and the value is a summary." 
      }

      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[body])

      json_format = json.loads(response.choices[0].message.content)
      print(json_format) 

      # Parse the response to a json format
      return json_format 

    except Exception as e:
      print(f"Error: {e}")

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




