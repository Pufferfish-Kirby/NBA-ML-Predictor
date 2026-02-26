import pandas as pd
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

#teams to ids {'Lakers': 1610612747, 'Thunder': 1610612760, 'Raptors': 1610612761, 'Magic': 1610612753, 'Pelicans': 1610612740, 
# 'Timberwolves': 1610612750, 'Pacers': 1610612754, 'Jazz': 1610612762, '76ers': 1610612755, 'Bulls': 1610612741, 
# 'Hornets': 1610612766, 'Grizzlies': 1610612763, 'Knicks': 1610612752, 'Mavericks': 1610612742, 
# 'Heat': 1610612748, 'Pistons': 1610612765, 'Cavaliers': 1610612739, 'Wizards': 1610612764, 'Nets': 1610612751, 
# 'Rockets': 1610612745, 'Bucks': 1610612749, 'Hawks': 1610612737, 'Celtics': 1610612738, 'Warriors': 1610612744, 
# 'Spurs': 1610612759, 'Nuggets': 1610612743, 'Kings': 1610612758, 'Trail Blazers': 1610612757, 'Clippers': 1610612746, 
# 'Suns': 1610612756}

df = pd.read_csv("data/csv/Games.csv")
# Lets create a mapping that will mapping team records and ids
year = df[df['gameDateTimeEst'].str.startswith('2024') | df['gameDateTimeEst'].str.startswith('2025')].copy() #i have to use | instead of or
teams_to_ids = year.set_index('hometeamName')['hometeamId'].to_dict()

# Now we create dict of teamID to a tuple (wins, gamesplayed, then we makes loses out of gamesplayed-wins)
cutoff_date = pd.to_datetime("2025-10-20 19:30:00", format='mixed', utc=True)
start_2024 = pd.to_datetime("2024-10-21 19:30:00", format='mixed', utc=True)
end_2024 = pd.to_datetime('2025-04-13 15:30:00', format='mixed', utc=True)
test_2024 = pd.to_datetime('2024-12-11 15:30:00', format='mixed', utc=True)
# 2023-2024 season dates
start_2023 = pd.to_datetime("2023-10-24 19:30:00", format='mixed', utc=True)
end_2023 = pd.to_datetime('2024-04-14 15:30:00', format='mixed', utc=True)

last_season_cutoff_date = pd.to_datetime("2024-10-21 19:30:00", format='mixed', utc=True)
df['gameDateTimeEst'] = pd.to_datetime(df['gameDateTimeEst'], format='mixed', utc=True)
year['gameDateTimeEst'] = pd.to_datetime(year['gameDateTimeEst'], format='mixed', utc=True)
current_season = df[df['gameDateTimeEst'] >= cutoff_date].copy()
last_season = df[(df['gameDateTimeEst'] >= start_2024) & (df['gameDateTimeEst'] <= end_2024)]
sample = df[(df['gameDateTimeEst'] >= start_2024) & (df['gameDateTimeEst'] <= test_2024)]
season_2023_2024 = df[(df['gameDateTimeEst'] >= start_2023) & (df['gameDateTimeEst'] <= end_2023)]

wins_to_games_played = {}
home_wins_to_games_played = {}
away_wins_to_games_played = {}
last_wins_to_games_played = {}
season_2023_2024_wins = {}

for index, row in current_season.iterrows(): # iterrows iterates over the rows. Index has to be there but I don't have to use it.
    h_id = row['hometeamId']
    a_id = row['awayteamId']
    h_score = row['homeScore']
    a_score = row['awayScore']

    if h_id not in home_wins_to_games_played:
        home_wins_to_games_played[h_id] = {'wins': 0, 'games_played': 0}
    if a_id not in away_wins_to_games_played:
        away_wins_to_games_played[a_id] = {'wins': 0, 'games_played': 0}
    if h_id not in wins_to_games_played:
        wins_to_games_played[h_id] = {'wins': 0, 'games_played': 0}
    if a_id not in wins_to_games_played:
        wins_to_games_played[a_id] = {'wins': 0, 'games_played': 0}
    
    home_wins_to_games_played[h_id]['games_played'] += 1
    away_wins_to_games_played[a_id]['games_played'] += 1
    wins_to_games_played[h_id]['games_played'] += 1
    wins_to_games_played[a_id]['games_played'] += 1

    if row['winner'] == h_id:
        home_wins_to_games_played[h_id]['wins'] += 1
        wins_to_games_played[h_id]['wins'] += 1
    elif row['winner'] == a_id:
        away_wins_to_games_played[a_id]['wins'] += 1
        wins_to_games_played[a_id]['wins'] += 1


for index, row in last_season.iterrows(): # iterrows iterates over the rows. Index has to be there but I don't have to use it.
    h_id = row['hometeamId']
    a_id = row['awayteamId']
    h_score = row['homeScore']
    a_score = row['awayScore']

    if h_id not in last_wins_to_games_played:
        last_wins_to_games_played[h_id] = {'wins': 0, 'games_played': 0}
    if a_id not in last_wins_to_games_played:
        last_wins_to_games_played[a_id] = {'wins': 0, 'games_played': 0}

    last_wins_to_games_played[h_id]['games_played'] += 1
    last_wins_to_games_played[a_id]['games_played'] += 1

    if row['winner'] == h_id:
        last_wins_to_games_played[h_id]['wins'] += 1
    elif row['winner'] == a_id:
        last_wins_to_games_played[a_id]['wins'] += 1

# Track wins for 2023-2024 season
for index, row in season_2023_2024.iterrows():
    h_id = row['hometeamId']
    a_id = row['awayteamId']

    if h_id not in season_2023_2024_wins:
        season_2023_2024_wins[h_id] = {'wins': 0, 'games_played': 0}
    if a_id not in season_2023_2024_wins:
        season_2023_2024_wins[a_id] = {'wins': 0, 'games_played': 0}

    season_2023_2024_wins[h_id]['games_played'] += 1
    season_2023_2024_wins[a_id]['games_played'] += 1

    if row['winner'] == h_id:
        season_2023_2024_wins[h_id]['wins'] += 1
    elif row['winner'] == a_id:
        season_2023_2024_wins[a_id]['wins'] += 1

# Calculate win percentage for 2023-2024 season
for id in season_2023_2024_wins:
    season_2023_2024_wins[id]['win%'] = round(season_2023_2024_wins[id]['wins'] / season_2023_2024_wins[id]['games_played'], 2)

for id in home_wins_to_games_played:
    home_wins_to_games_played[id]['win%'] = round(home_wins_to_games_played[id]['wins'] / home_wins_to_games_played[id]['games_played'], 2)
    away_wins_to_games_played[id]['win%'] = round(away_wins_to_games_played[id]['wins'] / away_wins_to_games_played[id]['games_played'], 2)
    wins_to_games_played[id]['win%'] = round(wins_to_games_played[id]['wins'] / wins_to_games_played[id]['games_played'], 2)
    home_wins_to_games_played[id]['games_left'] = 41 - home_wins_to_games_played[id]['games_played']
    away_wins_to_games_played[id]['games_left'] = 41 - away_wins_to_games_played[id]['games_played']
    wins_to_games_played[id]['games_left'] = 82 - wins_to_games_played[id]['games_played']
    wins_to_games_played[id]['remaining_wins'] = (last_wins_to_games_played[id]['wins'] - wins_to_games_played[id]['wins'])    

for id in home_wins_to_games_played:
    last_wins_to_games_played[id]['win%'] = round(last_wins_to_games_played[id]['wins'] / last_wins_to_games_played[id]['games_played'], 2)


team_stats = pd.read_csv("data/csv/TeamStatistics.csv")
team_stats['gameDateTimeEst'] = pd.to_datetime(team_stats['gameDateTimeEst'], format='mixed', utc=True)
current_season_stats = team_stats[team_stats['gameDateTimeEst'] >= cutoff_date].copy()
team_stats_summary = {}
opponent_stats_summary = {}


mapping = {
    'ppg': 'teamScore', 'apg': 'assists', 'bpg': 'blocks', 'spg': 'steals', 'fg%': 'fieldGoalsPercentage',
    '3fg%': 'threePointersPercentage', 'ft%': 'freeThrowsPercentage','fta': 'freeThrowsAttempted','rpg': 'reboundsTotal',
    'orpg': 'reboundsOffensive', 'drpg': 'reboundsDefensive', 'to': 'turnovers', 'fouls': 'foulsPersonal',
    'fastbreak_points': 'pointsFastBreak', 'second_chance_ppg': 'pointsSecondChance', 'ppg_off_turnovers': 'pointsFromTurnovers',
    'points_in_paint': 'pointsInThePaint'
}

for index, row in current_season_stats.iterrows():
    t_id = row['teamId']
    o_id = row['opponentTeamId']

    if t_id not in team_stats_summary:
        team_stats_summary[t_id] = {key: 0 for key in mapping}
        team_stats_summary[t_id]['games'] = 0
        
    if o_id not in opponent_stats_summary:
        opponent_stats_summary[o_id] = {key: 0 for key in mapping}
        opponent_stats_summary[o_id]['games'] = 0

    team_stats_summary[t_id]['games'] += 1
    opponent_stats_summary[o_id]['games'] += 1

    for key in mapping:
        team_stats_summary[t_id][key] += row[mapping[key]]

    for key in mapping:
        opponent_stats_summary[o_id][key] += row[mapping[key]]
for stats_dict in [team_stats_summary, opponent_stats_summary]:
    for tid in stats_dict:
        for key in mapping:
            if key != 'games':
                stats_dict[tid][key] = round(stats_dict[tid][key] / stats_dict[tid]['games'], 2)

metric_set = []
for team_id in wins_to_games_played:
    row = {}
    row['team_id'] = team_id 
    row["win_pct"] = wins_to_games_played[team_id]["win%"]
    row['wins'] = wins_to_games_played[team_id]["wins"]
    row['games_played'] = wins_to_games_played[team_id]["games_played"]
    row["games_left"] = wins_to_games_played[team_id]["games_left"]

    # home
    row["home_win_pct"] = home_wins_to_games_played[team_id]["win%"]

    # away
    row["away_win_pct"] = away_wins_to_games_played[team_id]["win%"]
    row["prior_year_win_pct"] = last_wins_to_games_played[team_id]["win%"]

    for t in team_stats_summary[team_id]:
        if t != 'games':
            row[t] = team_stats_summary[team_id][t]
    for s in opponent_stats_summary[team_id]:
        if s != 'games':
            row['opponent ' + s] = opponent_stats_summary[team_id][s]
    remaining_wins = wins_to_games_played[team_id]['remaining_wins']
    games_left = wins_to_games_played[team_id]['games_left']
    row['remaining_wins'] = remaining_wins

    metric_set.append(row)
final_summary = pd.DataFrame(metric_set)

# Now we can create a base model
final_summary.corr()["remaining_wins"].sort_values(ascending=False)
final_summary.to_csv('data/csv/summarized_data.csv')

#NOW WE HAVE TO DO THE SAME THING FOR 2025 DATA

sample_wins_to_games_played = {}
sample_home_wins_to_games_played = {}
sample_away_wins_to_games_played = {}

for index, row in sample.iterrows(): # iterrows iterates over the rows. Index has to be there but I don't have to use it.
    h_id = row['hometeamId']
    a_id = row['awayteamId']
    h_score = row['homeScore']
    a_score = row['awayScore']  

    if h_id not in sample_home_wins_to_games_played:
        sample_home_wins_to_games_played[h_id] = {'wins': 0, 'games_played': 0}
    if a_id not in sample_away_wins_to_games_played:
        sample_away_wins_to_games_played[a_id] = {'wins': 0, 'games_played': 0}
    if h_id not in sample_wins_to_games_played:
        sample_wins_to_games_played[h_id] = {'wins': 0, 'games_played': 0}
    if a_id not in sample_wins_to_games_played:
        sample_wins_to_games_played[a_id] = {'wins': 0, 'games_played': 0}
    
    sample_home_wins_to_games_played[h_id]['games_played'] += 1
    sample_away_wins_to_games_played[a_id]['games_played'] += 1
    sample_wins_to_games_played[h_id]['games_played'] += 1
    sample_wins_to_games_played[a_id]['games_played'] += 1

    if row['winner'] == h_id:
        sample_home_wins_to_games_played[h_id]['wins'] += 1
        sample_wins_to_games_played[h_id]['wins'] += 1
    elif row['winner'] == a_id:
        sample_away_wins_to_games_played[a_id]['wins'] += 1
        sample_wins_to_games_played[a_id]['wins'] += 1

for id in sample_home_wins_to_games_played:
    sample_home_wins_to_games_played[id]['win%'] = round(sample_home_wins_to_games_played[id]['wins'] / sample_home_wins_to_games_played[id]['games_played'], 2)
    sample_away_wins_to_games_played[id]['win%'] = round(sample_away_wins_to_games_played[id]['wins'] / sample_away_wins_to_games_played[id]['games_played'], 2)
    sample_wins_to_games_played[id]['win%'] = round(sample_wins_to_games_played[id]['wins'] / sample_wins_to_games_played[id]['games_played'], 2)
    sample_home_wins_to_games_played[id]['games_left'] = 41 - sample_home_wins_to_games_played[id]['games_played']
    sample_away_wins_to_games_played[id]['games_left'] = 41 - sample_away_wins_to_games_played[id]['games_played']
    sample_wins_to_games_played[id]['games_left'] = 82 - sample_wins_to_games_played[id]['games_played']

last_season_stats = team_stats[(team_stats['gameDateTimeEst'] >= start_2024) & (team_stats['gameDateTimeEst'] <= test_2024)].copy()
last_team_stats_summary = {}
last_opponent_stats_summary = {}

print(sample_wins_to_games_played)

mapping = {
    'ppg': 'teamScore', 'apg': 'assists', 'bpg': 'blocks', 'spg': 'steals', 'fg%': 'fieldGoalsPercentage',
    '3fg%': 'threePointersPercentage', 'ft%': 'freeThrowsPercentage','fta': 'freeThrowsAttempted','rpg': 'reboundsTotal',
    'orpg': 'reboundsOffensive', 'drpg': 'reboundsDefensive', 'to': 'turnovers', 'fouls': 'foulsPersonal',
    'fastbreak_points': 'pointsFastBreak', 'second_chance_ppg': 'pointsSecondChance', 'ppg_off_turnovers': 'pointsFromTurnovers',
    'points_in_paint': 'pointsInThePaint'
}

for index, row in last_season_stats.iterrows():
    t_id = row['teamId']
    o_id = row['opponentTeamId']

    if t_id not in last_team_stats_summary:
        last_team_stats_summary[t_id] = {key: 0 for key in mapping}
        last_team_stats_summary[t_id]['games'] = 0
        
    if o_id not in last_opponent_stats_summary:
        last_opponent_stats_summary[o_id] = {key: 0 for key in mapping}
        last_opponent_stats_summary[o_id]['games'] = 0

    last_team_stats_summary[t_id]['games'] += 1
    last_opponent_stats_summary[o_id]['games'] += 1

    for key in mapping:
        last_team_stats_summary[t_id][key] += row[mapping[key]]

    for key in mapping:
        last_opponent_stats_summary[o_id][key] += row[mapping[key]]
for stats_dict in [last_team_stats_summary, last_opponent_stats_summary]:
    for tid in stats_dict:
        for key in mapping:
            if key != 'games':
                stats_dict[tid][key] = round(stats_dict[tid][key] / stats_dict[tid]['games'], 2)

last_metric_set = []
for team_id in sample_wins_to_games_played:
    row = {}
    row['team_id'] = team_id 
    row["win_pct"] = sample_wins_to_games_played[team_id]["win%"]
    row['wins'] = sample_wins_to_games_played[team_id]["wins"]
    row['games_played'] = sample_wins_to_games_played[team_id]["games_played"]
    row["games_left"] = sample_wins_to_games_played[team_id]["games_left"]

    # home
    row["home_win_pct"] = sample_home_wins_to_games_played[team_id]["win%"]

    # away
    row["away_win_pct"] = sample_away_wins_to_games_played[team_id]["win%"]
    row["prior_year_win_pct"] = season_2023_2024_wins[team_id]["win%"]

    for t in last_team_stats_summary[team_id]:
        if t != 'games':
            row[t] = last_team_stats_summary[team_id][t]
    for s in last_opponent_stats_summary[team_id]:
        if s != 'games':
            row['opponent ' + s] = last_opponent_stats_summary[team_id][s]
    remaining_wins = (last_wins_to_games_played[team_id]['wins'] - sample_wins_to_games_played[team_id]['wins'])

    games_left = sample_wins_to_games_played[team_id]['games_left']
    row['remaining_wins'] = remaining_wins
    last_metric_set.append(row)

last_final_summary = pd.DataFrame(last_metric_set)
last_final_summary.corr()["remaining_wins"].sort_values(ascending=False)
last_final_summary.to_csv("data/csv/last_data.csv")

# Now we can create a base model in model.py