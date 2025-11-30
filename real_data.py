import time
from sqlalchemy import text
from utils.db_connection import get_engine
from utils.api_handler import fetch_recent_matches_list, fetch_match_scorecard
from datetime import datetime

def load_real_data():
    engine = get_engine()
    print("📡 Contacting Cricbuzz for Recent Matches...")
    data = fetch_recent_matches_list()
    
    match_list = []
    
    if 'typeMatches' in data:
        for m_type in data['typeMatches']:
            match_format = m_type.get('matchType', 'ODI')
            if 'seriesMatches' in m_type:
                for series in m_type['seriesMatches']:
                    series_name = series.get('seriesAdWrapper', {}).get('seriesName') or "Unknown Series"
                    matches_raw = series.get('seriesAdWrapper', {}).get('matches', []) or series.get('matches', [])
                    
                    for m in matches_raw:
                        match_info = m.get('matchInfo', {})
                        match_list.append({
                            "id": match_info.get('matchId'),
                            "desc": match_info.get('matchDesc'),
                            "series": series_name,
                            "format": match_format,
                            "date": datetime.fromtimestamp(int(match_info.get('startDate', 0))/1000).strftime('%Y-%m-%d'),
                            "venue": match_info.get('venueInfo', {}).get('ground'),
                            "city": match_info.get('venueInfo', {}).get('city'),
                            "country": match_info.get('venueInfo', {}).get('country'),
                            "t1": match_info.get('team1', {}).get('teamName'),
                            "t2": match_info.get('team2', {}).get('teamName'),
                            "winner": match_info.get('status')
                        })

    print(f"✅ Found {len(match_list)} matches via API. Merging into database...")

    with engine.connect() as conn:
        print("🔄 Refreshing 'Real' data partition...")
        conn.execute(text("DELETE FROM matches WHERE data_source = 'real'"))
        
        for m in match_list:
            exists = conn.execute(text("SELECT match_id FROM matches WHERE match_id=:mid"), {"mid": m['id']}).scalar()
            
            if not exists:
                print(f"   ➕ Adding Real Match: {m['t1']} vs {m['t2']}")
                conn.execute(text("""
                    INSERT INTO matches (
                        match_id, data_source, series_name, match_type, match_desc, 
                        venue_name, city, country, match_date, 
                        team1, team2, winner, 
                        win_margin_runs, win_margin_wickets, team1_country
                    ) VALUES (
                        :mid, 'real', :ser, :fmt, :desc, 
                        :ven, :city, :cnt, :date, 
                        :t1, :t2, :win, 
                        0, 0, :t1 -- Defaults for missing API fields
                    )
                """), {
                    "mid": m['id'], "ser": m['series'], "fmt": m['format'], "desc": m['desc'],
                    "ven": m['venue'], "city": m['city'], "cnt": m['country'], "date": m['date'],
                    "t1": m['t1'], "t2": m['t2'], "win": m['winner']
                })
                scard = fetch_match_scorecard(m['id'])
                if scard and 'scoreCard' in scard:
                    for innings in scard['scoreCard']:
                        if 'batTeamDetails' in innings and 'batsmenData' in innings['batTeamDetails']:
                            for bat in innings['batTeamDetails']['batsmenData'].values():
                                name = bat.get('batName')
                                runs = bat.get('runs', 0)
                                conn.execute(text("INSERT IGNORE INTO players (name, country, role) VALUES (:name, 'Unknown', 'Batsman')"), {"name": name})
                                pid = conn.execute(text("SELECT player_id FROM players WHERE name=:name"), {"name": name}).scalar()
                                conn.execute(text("""
                                    INSERT INTO player_performance (match_id, player_id, runs_scored, balls_faced)
                                    VALUES (:mid, :pid, :r, :b)
                                """), {"mid": m['id'], "pid": pid, "r": runs, "b": balls})

                time.sleep(1.0)        
        conn.commit()

    print("🚀 Real Data Merged Successfully!")

if __name__ == "__main__":
    load_real_data()
