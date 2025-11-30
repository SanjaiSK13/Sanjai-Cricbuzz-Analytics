import random
from datetime import datetime, timedelta
from sqlalchemy import text
from utils.db_connection import get_engine

NUM_MATCHES = 50 # Generates 50 matches at a time
TEAMS = ["India", "Australia", "England", "Pakistan", "South Africa", "New Zealand"]

VENUES_DATA = [
    ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
    ("MCG", "Melbourne", "Australia", 100024),
    ("Eden Gardens", "Kolkata", "India", 66000),
    ("Lord's", "London", "England", 30000),
    ("Newlands", "Cape Town", "South Africa", 25000),
    ("Gaddafi Stadium", "Lahore", "Pakistan", 27000)
]

PLAYERS_DATA = [
    ("Virat Kohli", "Batsman", "India"), ("Rohit Sharma", "Batsman", "India"),
    ("Jasprit Bumrah", "Bowler", "India"), ("Ravindra Jadeja", "All-rounder", "India"),
    ("Steve Smith", "Batsman", "Australia"), ("Pat Cummins", "Bowler", "Australia"),
    ("Ben Stokes", "All-rounder", "England"), ("Joe Root", "Batsman", "England"),
    ("Babar Azam", "Batsman", "Pakistan"), ("Shaheen Afridi", "Bowler", "Pakistan"),
    ("Kane Williamson", "Batsman", "New Zealand"), ("Trent Boult", "Bowler", "New Zealand"),
    ("Kagiso Rabada", "Bowler", "South Africa"), ("Quinton de Kock", "Wicketkeeper", "South Africa")
]

#Generate mock data in the required format for analysis
def generate_data_safely():
    engine = get_engine()
    
    with engine.connect() as conn:
        print("⏳ Appending Mock Data (Safe Mode)...")

        for v in VENUES_DATA:
            conn.execute(text("""
                INSERT IGNORE INTO venues (venue_name, city, country, capacity) 
                VALUES (:name, :city, :country, :cap)
            """), {"name": v[0], "city": v[1], "country": v[2], "cap": v[3]})

        player_map = {}
        for p_name, role, country in PLAYERS_DATA:
            # A. Insert into main PLAYERS table (for Analytics)
            conn.execute(text("""
                INSERT IGNORE INTO players (name, country, role, batting_style, bowling_style) 
                VALUES (:name, :cnt, :role, 'Right Hand', 'Fast')
            """), {"name": p_name, "cnt": country, "role": role})

            pid = conn.execute(text("SELECT player_id FROM players WHERE name=:name"), {"name": p_name}).scalar()
            player_map[p_name] = pid
            rand_matches = random.randint(50, 200)
            rand_runs = random.randint(2000, 10000)
            rand_avg = round(rand_runs / (rand_matches * 0.8), 2) # Approx avg
            
            conn.execute(text("""
                INSERT IGNORE INTO player_stats (player_id, player_name, matches, runs, average)
                VALUES (:pid, :name, :mat, :runs, :avg)
            """), {"pid": pid, "name": p_name, "mat": rand_matches, "runs": rand_runs, "avg": rand_avg})

        for i in range(1, NUM_MATCHES + 1):
            t1, t2 = random.sample(TEAMS, 2)
            venue = random.choice(VENUES_DATA)
            date = datetime.now() - timedelta(days=random.randint(0, 365))
            m_type = random.choice(["ODI", "T20", "Test"])
            winner = random.choice([t1, t2])

            m_id = random.randint(10000, 99999) 

            conn.execute(text("""
                INSERT IGNORE INTO matches (
                    match_id, data_source, series_name, match_type, match_desc, 
                    venue_name, city, country, match_date, 
                    team1, team2, winner, toss_winner, toss_decision,
                    win_margin_runs, win_margin_wickets, team1_country
                ) VALUES (
                    :mid, 'mock', :series, :mtype, 'Mock Match', 
                    :vname, :vcity, :vcnt, :date, 
                    :t1, :t2, :win, :t1, 'Bat',
                    10, 0, :t1
                )
            """), {
                "mid": m_id, "series": f"{t1} vs {t2}", "mtype": m_type,
                "vname": venue[0], "vcity": venue[1], "vcnt": venue[2], "date": date.strftime("%Y-%m-%d"),
                "t1": t1, "t2": t2, "win": winner
            })

            star = random.choice(list(player_map.keys()))
            pid = player_map[star]
            conn.execute(text("""
                INSERT INTO player_performance (match_id, player_id, runs_scored, balls_faced, wickets, runs_conceded, overs_bowled)
                VALUES (:mid, :pid, 50, 40, 0, 0, 0)
            """), {"mid": m_id, "pid": pid})
            
        conn.commit()
        print(f"🚀 Success! Added {NUM_MATCHES} matches. Mock players are now visible in CRUD.")

if __name__ == "__main__":
    generate_data_safely()
