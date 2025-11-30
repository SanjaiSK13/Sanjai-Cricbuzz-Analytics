QUESTION_BANK = {
    "Question 1": {
        "question": "Find all players who represent India.",
        "sql": "SELECT name, role, batting_style, bowling_style FROM players WHERE country = 'India';"
    },
    "Question 2": {
        "question": "Show all matches played in the last 30 days.",
        "sql": "SELECT series_name, team1, team2, venue_name, city, match_date FROM matches WHERE match_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) ORDER BY match_date DESC;"
    },
    "Question 3": {
        "question": "Top 10 highest run scorers in ODI cricket.",
        "sql": "SELECT p.name, SUM(pp.runs_scored) as total_runs, AVG(pp.runs_scored) as batting_avg FROM player_performance pp JOIN players p ON pp.player_id = p.player_id JOIN matches m ON pp.match_id = m.match_id WHERE m.match_type = 'ODI' GROUP BY p.name ORDER BY total_runs DESC LIMIT 10;"
    },
    "Question 4": {
        "question": "Cricket venues with capacity > 30,000.",
        "sql": "SELECT venue_name, city, country, capacity FROM venues WHERE capacity > 30000 ORDER BY capacity DESC;"
    },
    "Question 5": {
        "question": "Total wins per team.",
        "sql": "SELECT winner as team_name, COUNT(*) as total_wins FROM matches WHERE winner IS NOT NULL GROUP BY winner ORDER BY total_wins DESC;"
    },
    "Question 6": {
        "question": "Count players by role (Batsman, Bowler, etc).",
        "sql": "SELECT role, COUNT(*) as player_count FROM players GROUP BY role;"
    },
    "Question 7": {
        "question": "Highest individual score in each format.",
        "sql": "SELECT m.match_type, MAX(pp.runs_scored) as highest_score FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id GROUP BY m.match_type;"
    },
    "Question 8": {
        "question": "Series started in 2024.",
        "sql": "SELECT DISTINCT series_name, match_type, match_date FROM matches WHERE YEAR(match_date) = 2024;"
    },
    "Question 9": {
        "question": "All-rounders with >1000 runs AND >50 wickets.",
        "sql": "SELECT p.name, SUM(pp.runs_scored) as total_runs, SUM(pp.wickets) as total_wickets FROM player_performance pp JOIN players p ON pp.player_id = p.player_id GROUP BY p.name HAVING total_runs > 1000 AND total_wickets > 50;"
    },
    "Question 10": {
        "question": "Last 20 matches with winner details.",
        "sql": "SELECT series_name, team1, team2, winner, match_date, venue_name FROM matches ORDER BY match_date DESC LIMIT 20;"
    },
    "Question 11": {
        "question": "Player performance comparison across formats.",
        "sql": "SELECT p.name, m.match_type, SUM(pp.runs_scored) as runs FROM player_performance pp JOIN players p ON pp.player_id = p.player_id JOIN matches m ON pp.match_id = m.match_id GROUP BY p.name, m.match_type ORDER BY p.name;"
    },
    "Question 12": {
        "question": "Home vs Away performance analysis.",
        "sql": "SELECT team1 as team, SUM(CASE WHEN country = team1_country THEN 1 ELSE 0 END) as home_games, SUM(CASE WHEN country != team1_country THEN 1 ELSE 0 END) as away_games FROM matches GROUP BY team1;"
    },
    "Question 13": {
        "question": "Partnerships > 100 runs.",
        "sql": "SELECT p1.name as batsman_1, p2.name as batsman_2, pt.runs_scored, m.match_date FROM partnerships pt JOIN players p1 ON pt.player1_id = p1.player_id JOIN players p2 ON pt.player2_id = p2.player_id JOIN matches m ON pt.match_id = m.match_id WHERE pt.runs_scored >= 100;"
    },
    "Question 14": {
        "question": "Bowling economy rate by venue.",
        "sql": "SELECT p.name, m.venue_name, AVG(pp.runs_conceded / pp.overs_bowled) as economy_rate FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id JOIN players p ON pp.player_id = p.player_id WHERE pp.overs_bowled >= 4 GROUP BY p.name, m.venue_name HAVING COUNT(*) >= 3;"
    },
    "Question 15": {
        "question": "Players excelling in close matches (<50 runs margin).",
        "sql": "SELECT p.name, AVG(pp.runs_scored) as avg_runs_in_crunch FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id JOIN players p ON pp.player_id = p.player_id WHERE m.win_margin_runs < 50 AND m.win_margin_runs > 0 GROUP BY p.name ORDER BY avg_runs_in_crunch DESC;"
    },
    "Question 16": {
        "question": "Year-on-year batting stats since 2020.",
        "sql": "SELECT p.name, YEAR(m.match_date) as year, AVG(pp.runs_scored) as avg_runs FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id JOIN players p ON pp.player_id = p.player_id WHERE YEAR(m.match_date) >= 2020 GROUP BY p.name, YEAR(m.match_date) ORDER BY p.name, year;"
    },
    "Question 17": {
        "question": "Does winning the toss lead to winning the match?",
        "sql": "SELECT toss_decision, COUNT(*) as total_matches, SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as matches_won, (SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(*) * 100) as win_percentage FROM matches GROUP BY toss_decision;"
    },
    "Question 18": {
        "question": "Most economical bowlers in limited overs.",
        "sql": "SELECT p.name, SUM(pp.runs_conceded) / SUM(pp.overs_bowled) as career_economy FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id JOIN players p ON pp.player_id = p.player_id WHERE m.match_type IN ('ODI', 'T20') GROUP BY p.name HAVING SUM(pp.overs_bowled) > 20 ORDER BY career_economy ASC;"
    },
    "Question 19": {
        "question": "Batting consistency (Standard Deviation).",
        "sql": "SELECT p.name, AVG(pp.runs_scored) as avg_score, STDDEV(pp.runs_scored) as consistency_variability FROM player_performance pp JOIN players p ON pp.player_id = p.player_id GROUP BY p.name HAVING COUNT(*) > 10 ORDER BY consistency_variability ASC;"
    },
    "Question 20": {
        "question": "Format-wise batting average for veteran players.",
        "sql": "SELECT p.name, SUM(CASE WHEN m.match_type = 'Test' THEN 1 ELSE 0 END) as test_matches, AVG(CASE WHEN m.match_type = 'Test' THEN pp.runs_scored ELSE NULL END) as test_avg, SUM(CASE WHEN m.match_type = 'ODI' THEN 1 ELSE 0 END) as odi_matches, AVG(CASE WHEN m.match_type = 'ODI' THEN pp.runs_scored ELSE NULL END) as odi_avg FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id JOIN players p ON pp.player_id = p.player_id GROUP BY p.name HAVING COUNT(*) > 20;"
    },
    "Question 21": {
        "question": "Weighted Ranking System (Calculated Points).",
        "sql": "SELECT p.name, (SUM(pp.runs_scored) * 0.01) + (AVG(pp.runs_scored) * 0.5) + (SUM(pp.wickets) * 2) as mvp_score FROM player_performance pp JOIN players p ON pp.player_id = p.player_id GROUP BY p.name ORDER BY mvp_score DESC;"
    },
    "Question 22": {
        "question": "Head-to-Head Win % (Team A vs Team B).",
        "sql": "SELECT team1, team2, COUNT(*) as total_played, SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) as team1_wins, SUM(CASE WHEN winner = team2 THEN 1 ELSE 0 END) as team2_wins FROM matches GROUP BY team1, team2 HAVING total_played >= 5;"
    },
    "Question 23": {
        "question": "Player Form: Last 5 matches avg vs Last 10 matches avg.",
        "sql": "WITH PlayerStats AS (SELECT p.name, pp.runs_scored, ROW_NUMBER() OVER (PARTITION BY p.name ORDER BY m.match_date DESC) as match_rank FROM player_performance pp JOIN matches m ON pp.match_id = m.match_id JOIN players p ON pp.player_id = p.player_id) SELECT name, AVG(CASE WHEN match_rank <= 5 THEN runs_scored END) as last_5_avg, AVG(CASE WHEN match_rank <= 10 THEN runs_scored END) as last_10_avg FROM PlayerStats GROUP BY name;"
    },
    "Question 24": {
        "question": "Best Batting Partnerships (Success Rate).",
        "sql": """
        SELECT 
            p1.name as player_1, 
            p2.name as player_2, 
            AVG(pt.runs_scored) as avg_partnership,
            MAX(pt.runs_scored) as highest_partnership,
            COUNT(*) as partnerships_count
        FROM partnerships pt
        JOIN players p1 ON pt.player1_id = p1.player_id
        JOIN players p2 ON pt.player2_id = p2.player_id
        GROUP BY p1.name, p2.name
        HAVING COUNT(*) >= 1
        ORDER BY avg_partnership DESC;
        """
    },
    "Question 25": {
        "question": "Quarterly Performance Evolution (Time Series).",
        "sql": """
        SELECT 
            p.name,
            CONCAT(YEAR(m.match_date), '-Q', QUARTER(m.match_date)) as quarter,
            AVG(pp.runs_scored) as quarterly_avg
        FROM player_performance pp
        JOIN matches m ON pp.match_id = m.match_id
        JOIN players p ON pp.player_id = p.player_id
        GROUP BY p.name, quarter
        ORDER BY p.name, quarter;
        """
    }
}
