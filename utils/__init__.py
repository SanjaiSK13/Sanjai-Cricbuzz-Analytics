import sqlite3 as _sqlite3
import utils.db_connection as _db
import utils.api_helper as _api

# DB Passthrough
get_connection       = _db.get_connection
get_all_players      = _db.get_all_players
get_player_by_id     = _db.get_player_by_id
get_batting_stats    = _db.get_batting_stats
get_bowling_stats    = _db.get_bowling_stats
upsert_batting_stats = _db.upsert_batting_stats
upsert_bowling_stats = _db.upsert_bowling_stats
update_player        = _db.update_player
delete_player        = _db.delete_player
get_all_matches      = _db.get_all_matches
delete_match         = _db.delete_match
run_analytics_query  = _db.run_analytics_query
run_custom_query     = _db.run_custom_query

# Initialization
def init_db():
    return _db.init_database()

# DB Execution Helpers
def run_query(sql, params=()):
    df = _db.run_query(sql, params)
    if df is None or (hasattr(df, 'empty') and df.empty):
        return []
    return df.to_dict("records")

def run_write(sql, params=()):
    return _db.execute_write(sql, params)

def run_insert(sql, params=()):
    res = _db.execute_write(sql, params)
    return res.get("lastrowid") if res.get("success") else -1

# Dashboard & Metadata
def get_dashboard_stats():
    stats = _db.get_db_stats()
    # FIX: Ensure keys match the 'stats["total_players"]' calls in Home.py
    return {
        "total_players": stats.get("players", 0),
        "total_matches": stats.get("matches", 0),
        "total_teams":   stats.get("teams", 0),
        "total_venues":  stats.get("venues", 0),
        "live_matches":  0,  # Placeholder for UI consistency
        "upcoming":      0   # Placeholder for UI consistency
    }

def get_all_teams(): return _db.get_teams_dict()
def get_all_venues(): return _db.get_venues_dict()

# API Wrappers
def get_live_matches():
    data = _api.get_live_matches()
    return data.get("matches", [])

def get_upcoming_matches():
    data = _api.get_upcoming_matches()
    return data.get("matches", [])

def get_match_scorecard(match_id: str) -> dict:
    # Points to get_scorecard internally via api_helper alias
    return _api.get_scorecard(match_id)

def get_top_batting_stats(fmt="ODI"):
    fmt_map = {"TEST": "test", "ODI": "odi", "T20I": "t20"}
    data = _api.get_player_rankings("batsmen", fmt_map.get(fmt.upper(), "odi"))
    return data.get("players", [])

def get_top_bowling_stats(fmt="ODI"):
    fmt_map = {"TEST": "test", "ODI": "odi", "T20I": "t20"}
    data = _api.get_player_rankings("bowlers", fmt_map.get(fmt.upper(), "odi"))
    return data.get("players", [])

def get_current_series():
    # Fixes name mismatch for active series fetching
    data = _api.get_active_series()
    return data.get("series", [])

def check_api_status():
    return _api.check_api_status()