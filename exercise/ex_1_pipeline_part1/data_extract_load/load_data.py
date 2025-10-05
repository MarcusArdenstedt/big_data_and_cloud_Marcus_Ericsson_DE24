import requests
from dotenv import load_dotenv
from constants import API_KEY
import dlt 
from pathlib import Path


load_dotenv()

api_key = API_KEY
headers = {
    'x-apisports-key': api_key,
}
url = "https://v3.football.api-sports.io"

db_path = str(Path(__file__).parents[1] / "data_warehouse/football_player.duckdb")




def _get_url(endpoints, params):
    url_for_search = f"{url}/{endpoints}"
    response = requests.get(url_for_search, headers= headers, params= params)
    response.raise_for_status()
    return response.json()


def get_team_id(league_id = 113):
    
    endpoints = "/teams"

    params = {
        "league": league_id,
        "season": 2021,
    }
    df_team = _get_url(endpoints= endpoints, params= params)
    print(f"[DEBUG] antal lag hittade: {len(df_team["response"])}")
    return [team_id["team"]["id"] for team_id in df_team["response"]]


@dlt.resource(write_disposition= "replace")
def get_player_info(league_id = 113):

    teams_id = get_team_id(league_id= 113)
    
    for team_id in teams_id:
        # pagination: streaming each player at time and when there is no batch it will break the loop
        page = 1
        while True:
            params = {
                "team": team_id,
                "league": league_id,
                "season": 2021,
                "page": page
            }
    
            data = _get_url(endpoints= "/players", params= params)
            
            batch = data.get("response", [])
            
            if not batch:
                break 
            
            for player in batch:
                yield player 
            page += 1
            
            if (data.get("paging") or {}).get("current") == (data.get("paging") or {}).get("total"):
                break
            
            
def run_pipeline(table_name):
    pipeline = dlt.pipeline(
        pipeline_name = "swedish_fp",
        destination= dlt.destinations.duckdb(db_path),
        dataset_name= "staging",
    )
    
    load_info = pipeline.run(get_player_info(),table_name= table_name)
    print(load_info)
    
if __name__=="__main__":
    run_pipeline(table_name= "allsvenska_player")
    
