import os
import supabase
from supabase import create_client, Client
import environments

def insert_table(pdf, problem, solution, business_model, market_analysis, market_size, team, competitive_landscape, competitive_advantage, category):
    data, count = supabase.table('pitchdeck').insert(
        {
            "pitch_pdf": pdf,
            "pitch_problem": problem,
            "pitch_solution": solution,
            "pitch_business_model": business_model,
            "pitch_market_analysis": market_analysis,
            "pitch_market_size": market_size,
            "pitch_team": team,
            "pitch_competitive_landscape": competitive_landscape,
            "pitch_competitive_advantage": competitive_advantage,
            "pitch_category": category
        }).execute()

def get_table():
    return supabase.table('pitchdeck').select("*").execute()

if __name__ == "__main__":
    url = os.environ["SUPABASE_URL"]
    api_key = os.environ["SUPABASE_API_KEY"]

    supabase = create_client(url, api_key)

    # insert_table("123", "2", "123", "123", "123", "123", "123", "123", "123", "123")

    print(get_table().json())

