import pypdf 
import os 
import openai
import environments 

class Parser: 
  
  def __init__(self, filename): 
    self.filename = filename

  def _parse(self):
    # Parse all text content from the pdf file by page
    pdf = pypdf.PdfReader(open(self.filename, "rb"))
    content = []
    for page in pdf.pages:
      content.append([page.extract_text()])
    return content

  def get_criterias(self):

    # Based on the text content, extract the criterias if any based on open ai
    content = self._parse() 
    criterias = ["Category", "Problem Statement", "Solution", "Business Model", "Market Analysis", "Team"]

    # Compile the content based on criteria with open ai 
    try:
      openai.api_key = os.environ['OPENAI_API']
      body = {
        "role": "user",
        "content": f"Generate a summary of the document based on the following criterias: {criterias}. The content of the document is as follows: {content}. \nPlease generate the text in nicely formatted point forms based on the criterias. Also generate me streamlit code that can visualize the statistics with graphs at the end." 
      }

      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[body])

      # Extract the criterias from the response
      print(response.choices[0].message.content)
    except Exception as e:
      print(f"Error: {e}")
      
if __name__ == "__main__":
  parser = Parser("airbnb_pitch.pdf")
  parser.get_criterias()




