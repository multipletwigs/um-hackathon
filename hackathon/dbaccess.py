import os
from supabase import create_client, Client
import hashlib
import time

url = os.environ["SUPABASE_URL"] if os.environ["SUPABASE_URL"] is not None else st.secrets["SUPABASE_URL"]
api_key = os.environ["SUPABASE_API_KEY"] if os.environ["SUPABASE_API_KEY"] is not None else st.secrets["SUPABASE_API_KEY"]
supabase = create_client(url, api_key)

def insert_table(problem, solution, business_model, market_analysis, market_size, team, competitive_landscape, competitive_advantage, category, filehash):
    client = create_client(url, api_key) 
    response = client.table('pitchdeck').insert(
        {
            "pitch_problem": problem,
            "pitch_solution": solution,
            "pitch_business_model": business_model,
            "pitch_market_analysis": market_analysis,
            "pitch_market_size": market_size,
            "pitch_team": team,
            "pitch_competitive_landscape": competitive_landscape,
            "pitch_competitive_advantage": competitive_advantage,
            "pitch_category": category,
            "pitch_filehash": filehash
        }).execute()
    
    return response
    
def get_table():
    client = create_client(url, api_key)
    return client.table('pitchdeck').select("*").execute()

def get_row_by_hash(filehash):
    client = create_client(url, api_key)
    return client.table("pitchdeck").select("*").eq("pitch_filehash", filehash).execute()
    
def hash_file(filename):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(filename, "rb") as file:
        while True:
            data = file.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def hash_file_bytes(filebyte):
    BUF_SIZE = 65536
    
    sha256 = hashlib.sha256()
    
    while True:
        data = filebyte.read(BUF_SIZE)
        if not data:
            break
        sha256.update(data)     
    return sha256.hexdigest()
            
