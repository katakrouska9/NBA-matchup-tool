from nba_api.stats.endpoints import leaguegamefinder
from nba_api.live.nba.endpoints import scoreboard
from tabulate import tabulate
import pandas as pd

pd.set_option('display.max.columns', None)

#Get today's games
# 1. Get today's live scoreboard
board = scoreboard.ScoreBoard()
games_dict = board.get_dict() 
games_data = games_dict['scoreboard']['games']

# 2. Check each game's status and list the games

active_matches = []
match_numbers = []
print('Active matches are listed bellow -- What match would you like to follow?')

if not games_data:
    print("No active matches")
else:
    for i,game in enumerate(games_data,1):
        home_team = game['homeTeam']['teamName']
        away_team = game['awayTeam']['teamName']
        status = game['gameStatusText'] # This says "Live", "Final", or "7:30 PM"
        
        match_name= f"{away_team} vs {home_team}"
        active_matches.append(match_name)
        match_numbers.append(i)
        print(f"{i}. {away_team} vs {home_team} - Status: {status}")


#Interactive element
choice = input("\nSelect a match number to follow: ")

choice_int = int(choice)

if choice_int in match_numbers:
    print("Thanks!")
else:
    print("You selected wrong, try again.")
    choice = input("\nSelect a match number to follow: ")
    choice_int = int(choice)
    if choice_int in match_numbers:
        print("Thanks!")
    else:
        print("You selected wrong again, I am ending the script.")

choice_plug = choice_int-1
match_of_interest = active_matches[choice_plug]

teams = match_of_interest.split(" vs ")
home_team= teams[0]
away_team = teams[1]


#Looking in the history
# Finding all games since 4.3.2015
gamefinder = leaguegamefinder.LeagueGameFinder()
games = gamefinder.get_data_frames()[0]
games.sort_values('GAME_DATE', ascending = False)
#games[games['TEAM_ABBREVIATION'] == "AUS"]

# Translating team names to abbreviations
home_team_abr=games.loc[games['TEAM_NAME']== " "+ home_team,'TEAM_ABBREVIATION'].iloc[0]
#home_team_abr=games.loc[games['TEAM_NAME']== "Cleveland Cavaliers",'TEAM_ABBREVIATION'].iloc[0]
away_team_abr=games.loc[games['TEAM_NAME']== " "+ away_team,'TEAM_ABBREVIATION'].iloc[0]
#away_team_abr=games.loc[games['TEAM_NAME']== "Golden State Warriors",'TEAM_ABBREVIATION'].iloc[0]
match_code = home_team_abr + " vs. " + away_team_abr

#Cleaning the initial match list
games['MATCH_CLEAN'] = games['MATCHUP'].str.replace(' @ ', ' vs. ')

#Adding a competitor name

games['COMPETITOR'] = games.apply(lambda row: row['MATCH_CLEAN'].replace(row["TEAM_ABBREVIATION"],"").replace(" vs. ","").strip(),axis=1) #Creating a column for competitor - takes the match column and removes everything else than the competitor
team_map = games[['TEAM_NAME', 'TEAM_ABBREVIATION']].drop_duplicates().set_index('TEAM_ABBREVIATION')['TEAM_NAME'].to_dict() #Creates a lookup mapping for names
games['COMPETITOR_NAME'] = games['COMPETITOR'].map(team_map) #xlookup the names

games = games.rename(columns={'GAME_DATE':"Date", 'TEAM_NAME': "Team A", "WL":"Win/Loss","COMPETITOR_NAME": "Team B", "PLUS_MINUS": "Score difference","PTS": "Points scored", "FG_PCT":"Shots accuracy", 'FG3_PCT': "3-point accuracy"})
#games[games['TEAM_ABBREVIATION']== 'TMC']
#printing together matches
print("Here are their matches and stats:")
result = games[games['MATCH_CLEAN'] == match_code]
total_matches=len(result)
wins=int((result["Win/Loss"]== "W").sum())
win_pct = (wins/total_matches)*100

game_log = result[['Date', 'Team A', 'Team B', 'Win/Loss', 'Points scored', 'Score difference', 'Shots accuracy', '3-point accuracy']].head(10)
print(tabulate(game_log, headers='keys', tablefmt='psql', showindex=False))

print("Win percentage of " + str(home_team) + " is " + str(win_pct) + " %.")

print('hello')
print('hello'*3)

