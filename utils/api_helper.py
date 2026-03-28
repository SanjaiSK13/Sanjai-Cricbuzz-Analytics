import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Config
API_KEY  = os.getenv("RAPIDAPI_KEY", "")
API_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
BASE_URL = f"https://{API_HOST}"
TIMEOUT  = 10

HEADERS = {
    "X-RapidAPI-Key":  API_KEY,
    "X-RapidAPI-Host": API_HOST,
}

def _is_configured() -> bool:
    """True when a real API key has been set."""
    return bool(API_KEY) and API_KEY != "your_rapidapi_key_here"

# Generic request wrapper
def _get(endpoint: str, params: dict = None) -> dict:
    if not _is_configured():
        return {"error": "API key not configured"}
    try:
        url = f"{BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=HEADERS, params=params or {}, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Match Data
def get_live_matches() -> dict:
    raw = _get("matches/v1/live")
    if "error" in raw:
        return {"matches": _mock_live_matches(), "source": "mock", "error": raw["error"]}

    matches = []
    for item in raw.get("typeMatches", []):
        for series_match in item.get("seriesMatches", []):
            series_data = series_match.get("seriesAdWrapper", {})
            series_name = series_data.get("seriesName", "")
            for match in series_data.get("matches", []):
                mi = match.get("matchInfo", {})
                ms = match.get("matchScore", {})
                matches.append(_parse_match(mi, ms, series_name))
    return {"matches": matches, "source": "live", "error": ""}

def get_recent_matches() -> dict:
    raw = _get("matches/v1/recent")
    if "error" in raw:
        return {"matches": _mock_recent_matches(), "source": "mock", "error": raw["error"]}

    matches = []
    for item in raw.get("typeMatches", []):
        for series_match in item.get("seriesMatches", []):
            series_data = series_match.get("seriesAdWrapper", {})
            series_name = series_data.get("seriesName", "")
            for match in series_data.get("matches", []):
                mi = match.get("matchInfo", {})
                ms = match.get("matchScore", {})
                matches.append(_parse_match(mi, ms, series_name))
    return {"matches": matches[:20], "source": "live", "error": ""}

def get_upcoming_matches() -> dict:
    raw = _get("matches/v1/upcoming")
    if "error" in raw:
        return {"matches": _mock_upcoming_matches(), "source": "mock", "error": raw["error"]}

    matches = []
    for item in raw.get("typeMatches", []):
        for series_match in item.get("seriesMatches", []):
            series_data = series_match.get("seriesAdWrapper", {})
            series_name = series_data.get("seriesName", "")
            for match in series_data.get("matches", []):
                mi = match.get("matchInfo", {})
                matches.append(_parse_match(mi, {}, series_name))
    return {"matches": matches[:15], "source": "live", "error": ""}

def _parse_match(mi: dict, ms: dict, series_name: str = "") -> dict:
    team1 = mi.get("team1", {})
    team2 = mi.get("team2", {})
    venue = mi.get("venue", {})
    
    # Score formatting
    t1score = ms.get("team1Score", {})
    t2score = ms.get("team2Score", {})

    # Date formatting
    start_ts = mi.get("startDate")
    readable_date = ""
    if start_ts:
        try:
            dt_obj = datetime.fromtimestamp(int(start_ts)/1000)
            readable_date = dt_obj.strftime('%d %b, %H:%M')
        except:
            readable_date = "TBD"

    def fmt_innings(inn: dict) -> str:
        if not inn: return ""
        inngs_list = inn.get("inngs", [])
        if isinstance(inngs_list, dict): inngs_list = [inngs_list]
        return " | ".join([f"{i.get('r',0)}/{i.get('w',0)} ({i.get('o',0)} ov)" for i in inngs_list])

    return {
        "match_id": mi.get("matchId", ""),
        "description": mi.get("matchDesc", ""),
        "match_format": mi.get("matchFormat", ""),
        "series_name": series_name or mi.get("seriesName", ""),
        "status": mi.get("status", ""),
        "state": mi.get("state", ""),
        "team1_name": team1.get("teamName", ""),
        "team1_short": team1.get("teamSName", ""),
        "team2_name": team2.get("teamName", ""),
        "team2_short": team2.get("teamSName", ""),
        "venue_name": venue.get("groundName", ""),
        "venue_city": venue.get("city", ""),
        "venue_country": venue.get("country", ""),
        "team1_score": fmt_innings(t1score),
        "team2_score": fmt_innings(t2score),
        "start_date": readable_date,
    }

# Rankings & Series
def get_player_rankings(category: str = "batsmen", match_format: str = "odi") -> dict:
    raw = _get(f"stats/v1/rankings/{category}", {"formatType": match_format})
    if "error" in raw:
        return {"players": _mock_rankings(category, match_format), "source": "mock", "error": raw["error"]}

    players = []
    for p in raw.get("rank", [])[:20]:
        players.append({
            "rank": p.get("rank", ""),
            "name": p.get("name", ""),
            "country": p.get("country", ""),
            "rating": p.get("rating", ""),
            "player_id": p.get("id", ""),
        })
    return {"players": players, "source": "live", "error": ""}

def get_active_series() -> dict:
    raw = _get("series/v1/active")
    if "error" in raw:
        return {"series": _mock_series(), "source": "mock", "error": raw["error"]}

    series_list = []
    for item in raw.get("seriesMapProto", []):
        for s in item.get("series", []):
            series_list.append({
                "series_id": s.get("id", ""),
                "name": s.get("name", ""),
                "start_date": s.get("startDt", ""),
                "end_date": s.get("endDt", ""),
            })
    return {"series": series_list, "source": "live", "error": ""}

# Scorecard Data
def get_scorecard(match_id: str) -> dict:
    raw = _get(f"mcenter/v1/{match_id}/scard")
    if "error" in raw:
        return {"innings": _mock_scorecard(), "status": "Mock scorecard", "error": raw["error"]}

    innings_list = []
    for sc in raw.get("scoreCard", []):
        inning = {
            "title": sc.get("batTeamDetails", {}).get("batTeamName", ""),
            "batsmen": [], "bowlers": [],
            "extras": sc.get("extrasData", {}),
            "total": sc.get("scoreDetails", {}),
        }
        # Parse Batsmen
        bat_map = sc.get("batTeamDetails", {}).get("batsmenData", {})
        for _, b in bat_map.items():
            inning["batsmen"].append({
                "name": b.get("batName", ""), "runs": b.get("runs", 0),
                "balls": b.get("balls", 0), "fours": b.get("fours", 0),
                "sixes": b.get("sixes", 0), "strike_rate": b.get("strikeRate", 0),
                "dismissed": b.get("outDesc", "not out"),
            })
        # Parse Bowlers
        bowl_map = sc.get("bowlTeamDetails", {}).get("bowlersData", {})
        for _, b in bowl_map.items():
            inning["bowlers"].append({
                "name": b.get("bowlName", ""), "overs": b.get("overs", 0),
                "maidens": b.get("maidens", 0), "runs": b.get("runs", 0),
                "wickets": b.get("wickets", 0), "economy": b.get("economy", 0),
            })
        innings_list.append(inning)

    return {"innings": innings_list, "status": raw.get("status", ""), "error": ""}

# Mock Data Fallbacks
def _mock_live_matches(): return []
def _mock_recent_matches(): return []
def _mock_upcoming_matches(): return []
def _mock_scorecard(): return []
def _mock_rankings(cat, fmt): return []
def _mock_series(): return []

def check_api_status() -> dict:
    if not _is_configured():
        return {"connected": False, "source": "mock", "message": "API key not set."}
    result = _get("matches/v1/live")
    if "error" in result:
        return {"connected": False, "source": "mock", "message": result["error"]}
    return {"connected": True, "source": "live", "message": "Connected to Cricbuzz API"}

get_match_scorecard = get_scorecard