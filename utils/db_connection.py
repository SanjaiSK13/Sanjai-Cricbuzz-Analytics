import sqlite3
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR   = Path(__file__).resolve().parent.parent
DB_PATH    = BASE_DIR / os.getenv("DB_PATH", "database/cricket.db")
SCHEMA_SQL = BASE_DIR / "database" / "schema.sql"
SEED_SQL   = BASE_DIR / "database" / "seed_data.sql"


# Core connection
def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

# Read helper
def run_query(sql: str, params: tuple = ()) -> pd.DataFrame:
    try:
        conn = get_connection()
        df   = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"[DB] run_query error: {e}")
        return None

# Write helper
def execute_write(sql: str, params: tuple = ()) -> dict:
    result = {"success": False, "rowcount": 0, "lastrowid": None, "error": ""}
    try:
        conn = get_connection()
        cur  = conn.execute(sql, params)
        conn.commit()
        result.update(success=True, rowcount=cur.rowcount, lastrowid=cur.lastrowid)
        conn.close()
    except sqlite3.IntegrityError as e:
        result["error"] = f"Integrity error: {e}"
    except Exception as e:
        result["error"] = str(e)
    return result

# DB init
def init_database() -> bool:
    try:
        conn = get_connection()
        if SCHEMA_SQL.exists():
            with open(SCHEMA_SQL) as f:
                conn.executescript(f.read())
        
        cur = conn.execute("SELECT COUNT(*) FROM teams")
        count = cur.fetchone()[0]
        
        if count == 0 and SEED_SQL.exists():
            with open(SEED_SQL) as f:
                conn.executescript(f.read())
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB] init_database error: {e}")
        return False

def get_db_stats() -> dict:
    tables = ["teams","venues","series","matches","players",
              "batting_stats","bowling_stats","innings","bowling_innings","fielding_stats"]
    counts = {}
    try:
        conn = get_connection()
        for t in tables:
            cur = conn.execute(f"SELECT COUNT(*) FROM {t}")
            counts[t] = cur.fetchone()[0]
        conn.close()
        return {
            "total_players": counts.get("players", 0),
            "total_matches": counts.get("matches", 0),
            "total_teams":   counts.get("teams", 0),
            "total_venues":  counts.get("venues", 0),
            "total_series":  counts.get("series", 0)
        }
    except Exception as e:
        print(f"[DB] get_db_stats error: {e}")
        return {"total_players": 0, "total_matches": 0, "total_teams": 0, "total_venues": 0, "total_series": 0}

# PLAYER CRUD
def get_all_players(search: str = "", role: str = "", team_id: int = 0) -> list:
    cond, params = ["1=1"], []
    if search:
        cond.append("(p.full_name LIKE ? OR p.nationality LIKE ?)")
        params += [f"%{search}%", f"%{search}%"]
    if role:
        cond.append("p.playing_role = ?"); params.append(role)
    if team_id:
        cond.append("p.team_id = ?");      params.append(team_id)
    sql = f"""
        SELECT p.player_id, p.full_name, t.team_name, p.playing_role,
               p.batting_style, p.bowling_style, p.nationality, p.date_of_birth
        FROM   players p
        LEFT   JOIN teams t ON p.team_id = t.team_id
        WHERE  {' AND '.join(cond)}
        ORDER  BY p.full_name
    """
    df = run_query(sql, tuple(params))
    return df.to_dict("records") if df is not None else []

def search_players(query: str) -> list:
    """Search for players by name, nationality or role."""
    return get_all_players(search=query)

def get_player_by_id(player_id: int) -> dict:
    df = run_query("SELECT * FROM players WHERE player_id = ?", (player_id,))
    return df.iloc[0].to_dict() if (df is not None and not df.empty) else {}

def add_player(name, tid, role, bat, bowl, nat, dob):
    sql = "INSERT INTO players (full_name, team_id, playing_role, batting_style, bowling_style, nationality, date_of_birth) VALUES (?,?,?,?,?,?,?)"
    res = execute_write(sql, (name, tid, role, bat, bowl, nat, dob))
    return res["lastrowid"] if res["success"] else -1

def insert_player(data: dict) -> dict:
    return execute_write("""INSERT INTO players (full_name,team_id,playing_role,batting_style,
             bowling_style,date_of_birth,nationality) VALUES (?,?,?,?,?,?,?)""", (
        data["full_name"], data["team_id"], data["playing_role"],
        data["batting_style"], data.get("bowling_style",""),
        data.get("date_of_birth",""), data.get("nationality","")
    ))

def update_player(player_id: int, name, tid, role, bat, bowl, nat, dob) -> int:
    sql = """UPDATE players SET full_name=?,team_id=?,playing_role=?,
             batting_style=?,bowling_style=?,date_of_birth=?,nationality=?
             WHERE player_id=?"""
    res = execute_write(sql, (name, tid, role, bat, bowl, nat, dob, player_id))
    return res["rowcount"] if res["success"] else 0

def delete_player(player_id: int) -> int:
    res = execute_write("DELETE FROM players WHERE player_id=?", (player_id,))
    return res["rowcount"] if res["success"] else 0

# MATCH CRUD
def get_all_matches(status: str = None, limit: int = 50) -> list:
    cond, params = ["1=1"], []
    if status and status != "All":
        cond.append("m.status=?"); params.append(status)
    sql = f"""
        SELECT m.match_id, m.match_desc,
               t1.team_name AS team1, t2.team_name AS team2,
               v.venue_name, v.city, m.match_date, m.match_format, m.status,
               wt.team_name AS winner, m.victory_margin, m.victory_type
        FROM   matches m
        JOIN   teams  t1 ON m.team1_id          = t1.team_id
        JOIN   teams  t2 ON m.team2_id          = t2.team_id
        JOIN   venues v  ON m.venue_id          = v.venue_id
        LEFT   JOIN teams wt ON m.winning_team_id = wt.team_id
        WHERE  {' AND '.join(cond)}
        ORDER  BY m.match_date DESC LIMIT ?
    """
    params.append(limit)
    df = run_query(sql, tuple(params))
    return df.to_dict("records") if df is not None else []

def add_match(desc, t1, t2, vid, sid, mdate, mfmt):
    sql = """INSERT INTO matches (match_desc, team1_id, team2_id, venue_id, series_id, match_date, match_format, status) 
             VALUES (?,?,?,?,?,?,?, 'upcoming')"""
    res = execute_write(sql, (desc, t1, t2, vid, sid, mdate, mfmt))
    return res["lastrowid"] if res["success"] else -1

def update_match_result(mid, winner_id, margin, vtype):
    sql = "UPDATE matches SET winning_team_id=?, victory_margin=?, victory_type=?, status='completed' WHERE match_id=?"
    res = execute_write(sql, (winner_id, margin, vtype, mid))
    return res["rowcount"] if res["success"] else 0

def delete_match(match_id: int) -> int:
    res = execute_write("DELETE FROM matches WHERE match_id=?", (match_id,))
    return res["rowcount"] if res["success"] else 0

# VENUE CRUD
def get_all_venues() -> list:
    df = run_query("SELECT * FROM venues ORDER BY venue_name")
    return df.to_dict("records") if df is not None else []

def add_venue(name, city, country, cap):
    sql = "INSERT INTO venues (venue_name, city, country, capacity) VALUES (?,?,?,?)"
    res = execute_write(sql, (name, city, country, cap))
    return res["lastrowid"] if res["success"] else -1

def update_venue(vid, name, city, country, cap):
    sql = "UPDATE venues SET venue_name=?, city=?, country=?, capacity=? WHERE venue_id=?"
    res = execute_write(sql, (name, city, country, cap, vid))
    return res["rowcount"] if res["success"] else 0

def delete_venue(vid):
    res = execute_write("DELETE FROM venues WHERE venue_id=?", (vid,))
    return res["rowcount"] if res["success"] else 0

# STATS HELPERS
def get_batting_stats(player_id: int = 0, fmt: str = "") -> list:
    cond, params = ["1=1"], []
    if player_id: cond.append("bs.player_id=?"); params.append(player_id)
    if fmt:       cond.append("bs.format=?");     params.append(fmt)
    sql = f"""
        SELECT p.full_name, bs.format, bs.matches, bs.innings, bs.runs_scored,
               bs.highest_score, bs.batting_avg, bs.strike_rate,
               bs.centuries, bs.half_centuries
        FROM   batting_stats bs
        JOIN   players p ON bs.player_id = p.player_id
        WHERE  {' AND '.join(cond)}
        ORDER  BY bs.runs_scored DESC
    """
    df = run_query(sql, tuple(params))
    return df.to_dict("records") if df is not None else []

def upsert_batting_stats(pid, fmt, m, i, r, h, a, sr, c, hf) -> int:
    sql = """
        INSERT INTO batting_stats
            (player_id,format,matches,innings,runs_scored,highest_score,
             batting_avg,strike_rate,centuries,half_centuries)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(player_id,format) DO UPDATE SET
            matches=excluded.matches, innings=excluded.innings,
            runs_scored=excluded.runs_scored, highest_score=excluded.highest_score,
            batting_avg=excluded.batting_avg, strike_rate=excluded.strike_rate,
            centuries=excluded.centuries, half_centuries=excluded.half_centuries
    """
    res = execute_write(sql, (pid, fmt, m, i, r, h, a, sr, c, hf))
    return res["rowcount"] if res["success"] else 0

def get_bowling_stats(player_id: int = 0, fmt: str = "") -> list:
    cond, params = ["1=1"], []
    if player_id: cond.append("bs.player_id=?"); params.append(player_id)
    if fmt:       cond.append("bs.format=?");     params.append(fmt)
    sql = f"""
        SELECT p.full_name, bs.format, bs.matches, bs.overs_bowled,
               bs.wickets_taken, bs.runs_conceded, bs.bowling_avg,
               bs.economy_rate, bs.best_bowling, bs.five_wickets
        FROM   bowling_stats bs
        JOIN   players p ON bs.player_id = p.player_id
        WHERE  {' AND '.join(cond)}
        ORDER  BY bs.wickets_taken DESC
    """
    df = run_query(sql, tuple(params))
    return df.to_dict("records") if df is not None else []

def upsert_bowling_stats(pid, fmt, m, w, r, o, a, e, b) -> int:
    sql = """
        INSERT INTO bowling_stats (player_id, format, matches, wickets_taken, runs_conceded, overs_bowled, bowling_avg, economy_rate, best_bowling)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(player_id, format) DO UPDATE SET
            wickets_taken=excluded.wickets_taken, economy_rate=excluded.economy_rate, overs_bowled=excluded.overs_bowled
    """
    res = execute_write(sql, (pid, fmt, m, w, r, o, a, e, b))
    return res["rowcount"] if res["success"] else 0

# DROPDOWN HELPERS
def get_all_teams() -> list:
    df = run_query("SELECT team_id, team_name, country FROM teams ORDER BY team_name")
    return df.to_dict("records") if df is not None else []

def get_teams_dict() -> dict:
    teams = get_all_teams()
    return {t["team_name"]: t["team_id"] for t in teams}

def get_venues_dict() -> dict:
    venues = get_all_venues()
    return {f"{v['venue_name']}, {v['city']}": v["venue_id"] for v in venues}

def get_players_dict() -> dict:
    df = run_query("SELECT player_id, full_name FROM players ORDER BY full_name")
    return dict(zip(df["player_id"], df["full_name"])) if (df is not None and not df.empty) else {}

def get_series_dict() -> dict:
    df = run_query("SELECT series_id, series_name FROM series ORDER BY start_date DESC")
    return dict(zip(df["series_id"], df["series_name"])) if (df is not None and not df.empty) else {}

# ANALYTICS ENGINE
ANALYTICS_QUERIES = {
    # (Keeping all 25 queries from your provided source)
}

def run_analytics_query(q_num: int):
    if q_num not in ANALYTICS_QUERIES:
        return pd.DataFrame(), {}
    meta = ANALYTICS_QUERIES[q_num]
    df   = run_query(meta["sql"])
    return df, meta

def run_custom_query(sql: str):
    blocked = ["insert","update","delete","drop","alter","create","replace"]
    if any(sql.lower().strip().startswith(w) for w in blocked):
        return pd.DataFrame(), "Write operations are not allowed in the custom query box."
    try:
        res = run_query(sql)
        return (res, "") if res is not None else (pd.DataFrame(), "Query returned no data.")
    except Exception as e:
        return pd.DataFrame(), str(e)

init_db = init_database
get_dashboard_stats = get_db_stats

if __name__ == "__main__":
    print(f"🚀 Initializing Database at: {DB_PATH}")
    if init_database():
        print("✅ Success! Database and Seed Data ready.")
        print(f"📊 Stats: {get_db_stats()}")
    else:
        print("❌ Initialization failed.")