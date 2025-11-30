import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

DEMO_PROFILE = {
    "id": "255",
    "name": "Virat Kohli",
    "personalInfo": {
        "born": "Nov 05, 1988 (36 years)",
        "birthPlace": "Delhi",
        "height": "5 ft 9 in",
        "role": "Batsman",
        "battingStyle": "Right Handed Bat",
        "bowlingStyle": "Right-arm medium",
        "country": "India",
        "fullName": "Virat Kohli"
    },
    "teams": [{"teamName": "India"}, {"teamName": "Royal Challengers Bangalore"}, {"teamName": "Delhi"}],
    "faceImageId": "170661" 
}

#Fetches live matches data
def fetch_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            matches = []
            if 'typeMatches' in data:
                for match_type in data['typeMatches']:
                    if 'seriesMatches' in match_type:
                        for series in match_type['seriesMatches']:
                             if 'seriesAdWrapper' in series and 'matches' in series['seriesAdWrapper']:
                                for match in series['seriesAdWrapper']['matches']:
                                    matches.append({
                                        "Match Info": match['matchInfo']['matchDesc'],
                                        "Team 1": match['matchInfo']['team1']['teamName'],
                                        "Team 2": match['matchInfo']['team2']['teamName'],
                                        "Status": match['matchInfo']['status'],
                                        "Venue": match['matchInfo']['venueInfo']['city']
                                    })
            return pd.DataFrame(matches)
    except Exception as e:
        print(f"API Error: {e}")
    return pd.DataFrame()

#Fetch ICC rankings data
def fetch_icc_rankings(category="batsmen", format_type="test"):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/" + category
    querystring = {"formatType": format_type}
    try:
        response = requests.get(url, headers=HEADERS, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if 'rank' in data:
                return pd.DataFrame(data['rank'])
    except Exception:
        pass
    return pd.DataFrame()

#Fetch Recent matches data
def fetch_recent_matches_list():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {}

#Fetch scorecard data
def fetch_match_scorecard(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

#Fetch player details from the database and print
def search_player(name):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
    querystring = {"name": name}
    try:
        response = requests.get(url, headers=HEADERS, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if 'player' in data:
                return data['player']
        if response.status_code in [429, 401, 403]:
            return [{"id": "demo_1", "name": "Virat Kohli"}] 
    except Exception:
        pass
    return [{"id": "demo_1", "name": "Virat Kohli"}] 

#Fetch player profile from the database
def fetch_player_profile(player_id):
    if player_id == "demo_1":
        return DEMO_PROFILE
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass

    return DEMO_PROFILE
