from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
import pandas as pd

app = FastAPI()

# Enable CORS so React can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") # the read_root function to start the api
def root():
    return {"message": "Hello World"} # we want a json to store all of this data (with keys to values)

@app.get("/sample")
def sample():
    df = pd.read_csv("data/csv/team.csv")
    return df.head().to_dict(orient="records")

@app.get("/teams")
def get_teams():
    # Read predictions and create team ID to name mapping
    predicted_df = pd.read_csv("data/csv/predicted_data.csv")
    games_df = pd.read_csv("data/csv/theteams.csv")
    
    # Create mapping from team ID to team name (using home teams)
    team_id_to_name = games_df.set_index('IDs')['Names'].to_dict()
    
    # Add team names to predictions
    teams = []
    for _, row in predicted_df.iterrows():
        team_id = row['team_id']
        team_name = team_id_to_name.get(team_id, f"Team {team_id}")
        
        team_data = {
            'team_id': int(team_id),
            'team_name': team_name,
            'current_wins': int(row['wins']),
            'current_losses': int(row['games_played'] - row['wins']),
            'games_played': int(row['games_played']),
            'win_pct': float(row['win_pct']),
            'predicted_final_wins': int(row['final_wins']),
            'predicted_final_losses': int(row['final_losses']),
            'predicted_final_win_pct': float(row['final_win_pct']),
        }
        teams.append(team_data)
    
    # Sort by predicted final wins (descending)
    teams.sort(key=lambda x: x['predicted_final_wins'], reverse=True)
    
    return teams

# python -m uvicorn main:app --reload click this to run