import os 
import environment
import openai
class MemoGenerator:
    def __init__(self, memo):
        self.memo = memo

    def generate(self):
        openai.api_key = os.environ['OPENAI_API']
        body = {
          "role": "user",
          "content": f"Generate a investment memo for the following data points: {self.memo}." 
        }

        return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[body], stream=True)

if __name__ == "__main__":
    memo = MemoGenerator("Company Name: Apple")
    memo.generate()