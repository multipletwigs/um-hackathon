# UM Hackathon 2023 - Team it is what it is
This README provides instructions on how to run a Streamlit app, which is what powers our application PitchSync. Along with the steps to set up a virtual environment and install all the required dependencies from a `requirements.txt` file.

## Prerequisites

- Python 3.7 or higher installed on your system.
- `virtualenv` package installed (You can install it using `pip install virtualenv`).

## Setup

1. Clone the repository to your local machine:

   ```shell
   git clone <repository_url>
   ```

2. Switch into the `hackathon` project directory:
  
  ```shell
  cd <repository_name>
  cd hackathon
  ```
 
3. Install all requirements after activating a virtualenv.

  ```shell
  pip install -r requirements.txt
  ```
  
4. You'll need to use your own API keys here as Supabase and OpenAI api rotates publically available keys due to safety issues. Alternatively, just run our site here! https://multipletwigs-um-hackathon-hackathonapp-dyoaeb.streamlit.app/

5. Run our streamlit app

   ```shell
   streamlit run app.py
   ``` 


