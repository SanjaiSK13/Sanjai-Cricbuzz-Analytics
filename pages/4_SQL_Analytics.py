import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
# FIX: Import via the bridge to ensure all function names are correctly mapped
import utils

# Page config
st.set_page_config(
    page_title="SQL Analytics | Cricbuzz LiveStats",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).resolve().parent.parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

@st.cache_resource
def _init():
    utils.init_db()
    return True
_init()

_PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#21262d"),
    yaxis=dict(gridcolor="#21262d"),
)

# ALL 25 SQL QUERIES
QUERIES = {

    # BEGINNER

    "Q1 – Indian Players": {
        "level": "Beginner",
        "description": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "sql": """
SELECT p.full_name        AS "Player Name",
       p.playing_role     AS "Role",
       p.batting_style    AS "Batting Style",
       p.bowling_style    AS "Bowling Style",
       p.date_of_birth    AS "Date of Birth"
FROM   players p
JOIN   teams   t ON p.team_id = t.team_id
WHERE  t.team_name = 'India'
ORDER  BY p.full_name;
""",
    },

    "Q2 – Recent Matches": {
        "level": "Beginner",
        "description": "Show all cricket matches played in the last 180 days. Include description, team names, venue, and date.",
        "sql": """
SELECT m.match_desc                 AS "Match",
       t1.team_name                 AS "Team 1",
       t2.team_name                 AS "Team 2",
       v.venue_name || ', ' || v.city AS "Venue",
       m.match_date                 AS "Date",
       m.match_format               AS "Format",
       m.status                     AS "Status"
FROM   matches m
JOIN   teams  t1 ON m.team1_id  = t1.team_id
JOIN   teams  t2 ON m.team2_id  = t2.team_id
JOIN   venues v  ON m.venue_id  = v.venue_id
WHERE  m.match_date >= date('now', '-180 days')
ORDER  BY m.match_date DESC;
""",
    },

    "Q3 – Top ODI Run Scorers": {
        "level": "Beginner",
        "description": "List the top 10 highest run scorers in ODI cricket with average and centuries.",
        "sql": """
SELECT p.full_name                AS "Player",
       t.team_name                AS "Country",
       bs.runs_scored             AS "Total Runs",
       ROUND(bs.batting_avg, 2)   AS "Average",
       bs.centuries               AS "100s",
       bs.half_centuries          AS "50s",
       bs.matches                 AS "Matches"
FROM   batting_stats bs
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
WHERE  bs.format = 'ODI'
ORDER  BY bs.runs_scored DESC
LIMIT  10;
""",
    },

    "Q4 – Large Venues (>25,000)": {
        "level": "Beginner",
        "description": "Display all cricket venues with seating capacity over 25,000, ordered by largest first (10 venues).",
        "sql": """
SELECT venue_name  AS "Venue",
       city        AS "City",
       country     AS "Country",
       capacity    AS "Capacity"
FROM   venues
WHERE  capacity > 25000
ORDER  BY capacity DESC
LIMIT  10;
""",
    },

    "Q5 – Team Win Counts": {
        "level": "Beginner",
        "description": "Calculate how many matches each team has won. Show team name and total wins.",
        "sql": """
SELECT t.team_name          AS "Team",
       COUNT(m.match_id)    AS "Total Wins"
FROM   matches m
JOIN   teams   t ON m.winning_team_id = t.team_id
WHERE  m.status = 'completed'
GROUP  BY t.team_name
ORDER  BY COUNT(m.match_id) DESC;
""",
    },

    "Q6 – Players by Role": {
        "level": "Beginner",
        "description": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper).",
        "sql": """
SELECT playing_role   AS "Role",
       COUNT(*)       AS "Number of Players"
FROM   players
WHERE  playing_role IS NOT NULL
GROUP  BY playing_role
ORDER  BY COUNT(*) DESC;
""",
    },

    "Q7 – Highest Score per Format": {
        "level": "Beginner",
        "description": "Find the highest individual batting score achieved in each cricket format.",
        "sql": """
SELECT bs.format                          AS "Format",
       MAX(bs.highest_score)              AS "Highest Score",
       p.full_name                        AS "Player",
       t.team_name                        AS "Country"
FROM   batting_stats bs
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
GROUP  BY bs.format
ORDER  BY MAX(bs.highest_score) DESC;
""",
    },

    "Q8 – Series Starting in 2024": {
        "level": "Beginner",
        "description": "Show all cricket series that started in 2024.",
        "sql": """
SELECT series_name    AS "Series",
       host_country   AS "Host Country",
       match_type     AS "Format",
       start_date     AS "Start Date",
       end_date       AS "End Date",
       total_matches  AS "Total Matches"
FROM   series
WHERE  strftime('%Y', start_date) = '2024'
ORDER  BY start_date;
""",
    },

    # INTERMEDIATE

    "Q9 – All-Rounder Greats": {
        "level": "Intermediate",
        "description": "Find all-rounders with 1000+ runs AND 50+ wickets across any format.",
        "sql": """
SELECT p.full_name             AS "Player",
       t.team_name             AS "Country",
       bs.format               AS "Format",
       bs.runs_scored          AS "Runs",
       bw.wickets_taken        AS "Wickets",
       ROUND(bs.batting_avg,2) AS "Bat Avg",
       ROUND(bw.bowling_avg,2) AS "Bowl Avg"
FROM   batting_stats bs
JOIN   bowling_stats bw ON bs.player_id = bw.player_id
                        AND bs.format   = bw.format
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
WHERE  bs.runs_scored   > 1000
  AND  bw.wickets_taken > 50
ORDER  BY bs.runs_scored DESC;
""",
    },

    "Q10 – Last 20 Results": {
        "level": "Intermediate",
        "description": "Get the last 20 completed matches with winner, margin, and venue.",
        "sql": """
SELECT m.match_desc                         AS "Match",
       t1.team_name                         AS "Team 1",
       t2.team_name                         AS "Team 2",
       wt.team_name                         AS "Winner",
       m.victory_margin || ' ' || m.victory_type AS "Result",
       v.venue_name || ', ' || v.city       AS "Venue",
       m.match_date                         AS "Date",
       m.match_format                       AS "Format"
FROM   matches m
JOIN   teams  t1 ON m.team1_id        = t1.team_id
JOIN   teams  t2 ON m.team2_id        = t2.team_id
LEFT JOIN teams wt ON m.winning_team_id = wt.team_id
JOIN   venues  v  ON m.venue_id       = v.venue_id
WHERE  m.status = 'completed'
ORDER  BY m.match_date DESC
LIMIT  20;
""",
    },

    "Q11 – Cross-format Batting": {
        "level": "Intermediate",
        "description": "Compare each player's runs across Test, ODI, and T20I (min 2 formats).",
        "sql": """
SELECT p.full_name AS "Player",
       t.team_name AS "Country",
       MAX(CASE WHEN bs.format = 'Test' THEN bs.runs_scored END) AS "Test Runs",
       MAX(CASE WHEN bs.format = 'ODI'  THEN bs.runs_scored END) AS "ODI Runs",
       MAX(CASE WHEN bs.format = 'T20I' THEN bs.runs_scored END) AS "T20I Runs",
       ROUND(AVG(bs.batting_avg), 2)                             AS "Overall Avg"
FROM   batting_stats bs
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
GROUP  BY p.player_id, p.full_name, t.team_name
HAVING COUNT(DISTINCT bs.format) >= 2
ORDER  BY COALESCE(MAX(CASE WHEN bs.format='Test' THEN bs.runs_scored END),0)
        + COALESCE(MAX(CASE WHEN bs.format='ODI'  THEN bs.runs_scored END),0)
        + COALESCE(MAX(CASE WHEN bs.format='T20I' THEN bs.runs_scored END),0) DESC;
""",
    },

    "Q12 – Home vs Away Performance": {
        "level": "Intermediate",
        "description": "Analyse each team's win record when playing at home vs away.",
        "sql": """
SELECT t.team_name AS "Team",
       SUM(CASE WHEN m.winning_team_id = t.team_id
                 AND v.country = t.country THEN 1 ELSE 0 END) AS "Home Wins",
       SUM(CASE WHEN m.winning_team_id = t.team_id
                 AND v.country <> t.country THEN 1 ELSE 0 END) AS "Away Wins",
       SUM(CASE WHEN (m.team1_id = t.team_id OR m.team2_id = t.team_id)
                 AND v.country = t.country THEN 1 ELSE 0 END)  AS "Home Matches",
       SUM(CASE WHEN (m.team1_id = t.team_id OR m.team2_id = t.team_id)
                 AND v.country <> t.country THEN 1 ELSE 0 END) AS "Away Matches"
FROM   teams t
JOIN   matches m ON (m.team1_id = t.team_id OR m.team2_id = t.team_id)
JOIN   venues  v ON m.venue_id  = v.venue_id
WHERE  m.status = 'completed'
GROUP  BY t.team_id, t.team_name
HAVING (SUM(CASE WHEN m.winning_team_id = t.team_id THEN 1 ELSE 0 END)) > 0
ORDER  BY "Home Wins" DESC;
""",
    },

    "Q13 – 100+ Partnerships": {
        "level": "Intermediate",
        "description": "Identify batting partnerships where two consecutive batsmen scored 100+ combined runs in the same innings.",
        "sql": """
SELECT p1.full_name    AS "Batsman 1",
       p2.full_name    AS "Batsman 2",
       (i1.runs_scored + i2.runs_scored) AS "Partnership Runs",
       i1.innings_number                 AS "Innings",
       m.match_desc                      AS "Match",
       m.match_date                      AS "Date"
FROM   innings i1
JOIN   innings i2 ON  i1.match_id       = i2.match_id
                  AND i1.innings_number  = i2.innings_number
                  AND i2.batting_position = i1.batting_position + 1
JOIN   players p1 ON i1.player_id = p1.player_id
JOIN   players p2 ON i2.player_id = p2.player_id
JOIN   matches m  ON i1.match_id  = m.match_id
WHERE  (i1.runs_scored + i2.runs_scored) >= 100
ORDER  BY (i1.runs_scored + i2.runs_scored) DESC;
""",
    },

    "Q14 – Bowling at Venues": {
        "level": "Intermediate",
        "description": "For bowlers who played at least 3 matches at the same venue (min 4 overs), show economy and wickets.",
        "sql": """
SELECT p.full_name              AS "Bowler",
       t.team_name              AS "Country",
       v.venue_name             AS "Venue",
       COUNT(bi.bowling_innings_id)         AS "Matches",
       ROUND(AVG(bi.economy_rate), 2)       AS "Avg Economy",
       SUM(bi.wickets_taken)                AS "Total Wickets",
       ROUND(AVG(bi.overs_bowled), 1)       AS "Avg Overs"
FROM   bowling_innings bi
JOIN   players p ON bi.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
JOIN   matches m ON bi.match_id  = m.match_id
JOIN   venues  v ON m.venue_id   = v.venue_id
WHERE  bi.overs_bowled >= 4
GROUP  BY bi.player_id, m.venue_id
HAVING COUNT(bi.bowling_innings_id) >= 3
ORDER  BY "Total Wickets" DESC;
""",
    },

    "Q15 – Close Match Heroes": {
        "level": "Intermediate",
        "description": "Players who perform in close matches (decided by <50 runs or <5 wickets).",
        "sql": """
SELECT p.full_name                    AS "Player",
       t.team_name                    AS "Country",
       COUNT(i.innings_id)            AS "Close Matches",
       ROUND(AVG(i.runs_scored), 2)   AS "Avg Runs",
       SUM(CASE WHEN m.winning_team_id = p.team_id THEN 1 ELSE 0 END) AS "Won"
FROM   innings i
JOIN   players p ON i.player_id = p.player_id
JOIN   teams   t ON p.team_id   = t.team_id
JOIN   matches m ON i.match_id  = m.match_id
WHERE  m.status = 'completed'
  AND  (
         (m.victory_type = 'runs'    AND CAST(m.victory_margin AS INTEGER) < 50)
      OR (m.victory_type = 'wickets' AND CAST(m.victory_margin AS INTEGER) < 5)
  )
GROUP  BY i.player_id
HAVING COUNT(i.innings_id) >= 2
ORDER  BY ROUND(AVG(i.runs_scored), 2) DESC;
""",
    },

    "Q16 – Year-on-Year Form": {
        "level": "Intermediate",
        "description": "Track player batting performance changes year by year since 2020 (min 5 matches/year).",
        "sql": """
SELECT p.full_name                       AS "Player",
       strftime('%Y', i.match_date)      AS "Year",
       COUNT(i.innings_id)               AS "Innings",
       ROUND(AVG(i.runs_scored), 2)      AS "Avg Runs",
       ROUND(AVG(i.strike_rate), 1)      AS "Avg Strike Rate",
       MAX(i.runs_scored)                AS "Best Score"
FROM   innings i
JOIN   players p ON i.player_id = p.player_id
WHERE  i.match_date >= '2020-01-01'
  AND  i.match_date IS NOT NULL
GROUP  BY i.player_id, strftime('%Y', i.match_date)
HAVING COUNT(i.innings_id) >= 2
ORDER  BY p.full_name, "Year";
""",
    },

    # ADVANCED

    "Q17 – Toss Advantage": {
        "level": "Advanced",
        "description": "Investigate whether winning the toss gives a win advantage, broken down by bat/bowl decision.",
        "sql": """
SELECT m.toss_decision                AS "Toss Decision",
       COUNT(*)                       AS "Total Matches",
       SUM(CASE WHEN m.toss_winner_id = m.winning_team_id THEN 1 ELSE 0 END)
                                      AS "Toss Winner Won",
       ROUND(
         100.0 * SUM(CASE WHEN m.toss_winner_id = m.winning_team_id THEN 1 ELSE 0 END)
         / COUNT(*), 1
       )                                             AS "Win % After Toss"
FROM   matches m
WHERE  m.status       = 'completed'
  AND  m.toss_winner_id IS NOT NULL
  AND  m.winning_team_id IS NOT NULL
  AND  m.toss_decision  IS NOT NULL
GROUP  BY m.toss_decision
ORDER  BY "Win % After Toss" DESC;
""",
    },

    "Q18 – Most Economical Bowlers": {
        "level": "Advanced",
        "description": "Best economy rate in ODI & T20I (min 10 matches, avg 2+ overs per match).",
        "sql": """
SELECT p.full_name              AS "Bowler",
       t.team_name              AS "Country",
       bs.format                AS "Format",
       bs.matches               AS "Matches",
       bs.wickets_taken         AS "Wickets",
       ROUND(bs.economy_rate,2) AS "Economy Rate",
       ROUND(bs.bowling_avg,2)  AS "Bowling Avg",
       bs.best_bowling          AS "Best"
FROM   bowling_stats bs
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
WHERE  bs.format IN ('ODI','T20I')
  AND  bs.matches >= 10
  AND  bs.overs_bowled / bs.matches >= 2
ORDER  BY bs.economy_rate ASC
LIMIT  15;
""",
    },

    "Q19 – Batting Consistency": {
        "level": "Advanced",
        "description": "Calculate standard deviation of scores per player since 2022 (lower = more consistent). Min 10 balls per innings.",
        "sql": """
SELECT p.full_name                  AS "Player",
       t.team_name                  AS "Country",
       COUNT(i.innings_id)          AS "Innings",
       ROUND(AVG(i.runs_scored),2)  AS "Average",
       ROUND(
         SQRT(AVG(i.runs_scored * i.runs_scored)
              - AVG(i.runs_scored) * AVG(i.runs_scored)),
         2
       )                            AS "Std Deviation",
       MAX(i.runs_scored)           AS "Best",
       MIN(i.runs_scored)           AS "Lowest"
FROM   innings i
JOIN   players p ON i.player_id = p.player_id
JOIN   teams   t ON p.team_id   = t.team_id
WHERE  i.balls_faced  >= 10
  AND  i.match_date   >= '2022-01-01'
GROUP  BY i.player_id
HAVING COUNT(i.innings_id) >= 3
ORDER  BY "Std Deviation" ASC;
""",
    },

    "Q20 – Multi-format Participation": {
        "level": "Advanced",
        "description": "Count matches per player per format with batting averages (min 20 total matches).",
        "sql": """
SELECT p.full_name AS "Player",
       t.team_name AS "Country",
       SUM(CASE WHEN bs.format='Test' THEN bs.matches ELSE 0 END) AS "Test Matches",
       SUM(CASE WHEN bs.format='ODI'  THEN bs.matches ELSE 0 END) AS "ODI Matches",
       SUM(CASE WHEN bs.format='T20I' THEN bs.matches ELSE 0 END) AS "T20I Matches",
       SUM(bs.matches)                                             AS "Total Matches",
       ROUND(MAX(CASE WHEN bs.format='Test' THEN bs.batting_avg END),2) AS "Test Avg",
       ROUND(MAX(CASE WHEN bs.format='ODI'  THEN bs.batting_avg END),2) AS "ODI Avg",
       ROUND(MAX(CASE WHEN bs.format='T20I' THEN bs.batting_avg END),2) AS "T20I Avg"
FROM   batting_stats bs
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
GROUP  BY p.player_id
HAVING SUM(bs.matches) >= 20
ORDER  BY SUM(bs.matches) DESC;
""",
    },

    "Q21 – Performance Ranking": {
        "level": "Advanced",
        "description": "Weighted composite score: batting + bowling + fielding. Ranked by format.",
        "sql": """
WITH bat_pts AS (
    SELECT player_id, format,
           ROUND(
             (runs_scored * 0.01)
             + (batting_avg  * 0.5)
             + (strike_rate  * 0.3),
           2) AS bat_score
    FROM batting_stats
),
bowl_pts AS (
    SELECT player_id, format,
           ROUND(
             (wickets_taken * 2)
             + ((50 - COALESCE(bowling_avg,50)) * 0.5)
             + ((6  - COALESCE(economy_rate,6)) * 2),
           2) AS bowl_score
    FROM bowling_stats
),
field_pts AS (
    SELECT player_id,
           ROUND((catches * 1.5) + (stumpings * 2) + (run_outs * 1), 2) AS field_score
    FROM fielding_stats
)
SELECT p.full_name  AS "Player",
       t.team_name  AS "Country",
       bp.format    AS "Format",
       COALESCE(bp.bat_score,0)    AS "Bat Points",
       COALESCE(bwp.bowl_score,0)  AS "Bowl Points",
       COALESCE(fp.field_score,0)  AS "Field Points",
       ROUND(
         COALESCE(bp.bat_score,0)
         + COALESCE(bwp.bowl_score,0)
         + COALESCE(fp.field_score,0),
       2)                          AS "Total Score",
       RANK() OVER (
         PARTITION BY bp.format
         ORDER BY COALESCE(bp.bat_score,0)
                + COALESCE(bwp.bowl_score,0)
                + COALESCE(fp.field_score,0) DESC
       )                           AS "Rank"
FROM   bat_pts bp
JOIN   players p  ON bp.player_id = p.player_id
JOIN   teams   t  ON p.team_id    = t.team_id
LEFT JOIN bowl_pts  bwp ON bp.player_id = bwp.player_id AND bp.format = bwp.format
LEFT JOIN field_pts fp  ON bp.player_id = fp.player_id
ORDER  BY bp.format, "Rank"
LIMIT  30;
""",
    },

    "Q22 – Head-to-Head Analysis": {
        "level": "Advanced",
        "description": "For team pairs with 5+ matches in the last 3 years, calculate win % and average victory margin.",
        "sql": """
WITH h2h AS (
    SELECT CASE WHEN t1.team_name < t2.team_name
                THEN t1.team_name ELSE t2.team_name END AS team_a,
           CASE WHEN t1.team_name < t2.team_name
                THEN t2.team_name ELSE t1.team_name END AS team_b,
           m.match_id,
           wt.team_name AS winner,
           m.victory_margin,
           m.victory_type
    FROM   matches m
    JOIN   teams t1 ON m.team1_id       = t1.team_id
    JOIN   teams t2 ON m.team2_id       = t2.team_id
    LEFT JOIN teams wt ON m.winning_team_id = wt.team_id
    WHERE  m.status = 'completed'
      AND  m.match_date >= date('now', '-3 years')
)
SELECT team_a                          AS "Team A",
       team_b                          AS "Team B",
       COUNT(*)                        AS "Matches",
       SUM(CASE WHEN winner=team_a THEN 1 ELSE 0 END)     AS "Team A Wins",
       SUM(CASE WHEN winner=team_b THEN 1 ELSE 0 END)     AS "Team B Wins",
       ROUND(
         100.0 * SUM(CASE WHEN winner=team_a THEN 1 ELSE 0 END) / COUNT(*),
       1)                                              AS "Team A Win%"
FROM   h2h
GROUP  BY team_a, team_b
HAVING COUNT(*) >= 2
ORDER  BY "Matches" DESC;
""",
    },

    "Q23 – Player Form Analysis": {
        "level": "Advanced",
        "description": "Analyse each player's last 10 innings and categorise as Excellent / Good / Average / Poor Form.",
        "sql": """
WITH recent AS (
    SELECT player_id,
           runs_scored,
           strike_rate,
           ROW_NUMBER() OVER (
             PARTITION BY player_id ORDER BY match_date DESC
           ) AS rn
    FROM innings
    WHERE match_date IS NOT NULL
),
last10 AS (
    SELECT player_id,
           AVG(runs_scored)                                  AS avg_last10,
           AVG(CASE WHEN rn <= 5 THEN runs_scored END)       AS avg_last5,
           AVG(strike_rate)                                  AS avg_sr,
           SUM(CASE WHEN runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_plus,
           SQRT(
             AVG(runs_scored*runs_scored) - AVG(runs_scored)*AVG(runs_scored)
           )                                                 AS std_dev
    FROM   recent
    WHERE  rn <= 10
    GROUP  BY player_id
    HAVING COUNT(*) >= 3
)
SELECT p.full_name                            AS "Player",
       t.team_name                            AS "Country",
       ROUND(l.avg_last10, 2)                 AS "Avg Last 10",
       ROUND(l.avg_last5, 2)                  AS "Avg Last 5",
       ROUND(l.avg_sr, 1)                     AS "Strike Rate",
       l.fifties_plus                         AS "50+ Scores",
       ROUND(l.std_dev, 2)                    AS "Consistency (SD)",
       CASE
         WHEN l.avg_last5 >= 50  THEN 'Excellent Form'
         WHEN l.avg_last5 >= 35  THEN 'Good Form'
         WHEN l.avg_last5 >= 20  THEN 'Average Form'
         ELSE                         'Poor Form'
       END                                    AS "Form Category"
FROM   last10 l
JOIN   players p ON l.player_id = p.player_id
JOIN   teams   t ON p.team_id   = t.team_id
ORDER  BY l.avg_last5 DESC;
""",
    },

    "Q24 – Best Batting Partnerships": {
        "level": "Advanced",
        "description": "Study successful batting partnerships. Pairs with 5+ innings together, avg partnership and success rate.",
        "sql": """
WITH pairs AS (
    SELECT i1.player_id AS pid1,
           i2.player_id AS pid2,
           (i1.runs_scored + i2.runs_scored) AS partnership
    FROM   innings i1
    JOIN   innings i2 ON  i1.match_id       = i2.match_id
                      AND i1.innings_number  = i2.innings_number
                      AND i2.batting_position = i1.batting_position + 1
)
SELECT p1.full_name                       AS "Batsman 1",
       p2.full_name                       AS "Batsman 2",
       COUNT(*)                           AS "Partnerships",
       ROUND(AVG(pr.partnership), 1)      AS "Avg Partnership",
       MAX(pr.partnership)                AS "Best Partnership",
       SUM(CASE WHEN pr.partnership >= 50 THEN 1 ELSE 0 END) AS "50+ Partnerships",
       ROUND(
         100.0 * SUM(CASE WHEN pr.partnership >= 50 THEN 1 ELSE 0 END) / COUNT(*),
       1)                                 AS "Success Rate %"
FROM   pairs pr
JOIN   players p1 ON pr.pid1 = p1.player_id
JOIN   players p2 ON pr.pid2 = p2.player_id
GROUP  BY pr.pid1, pr.pid2
HAVING COUNT(*) >= 2
ORDER  BY "Avg Partnership" DESC
LIMIT  15;
""",
    },

    "Q25 – Career Trajectory": {
        "level": "Advanced",
        "description": "Quarterly batting performance trend. Categorise as Career Ascending / Declining / Stable.",
        "sql": """
WITH quarterly AS (
    SELECT player_id,
           strftime('%Y', match_date) || '-Q'
           || CAST(((CAST(strftime('%m', match_date) AS INTEGER) - 1) / 3) + 1
              AS TEXT)                         AS quarter,
           AVG(runs_scored)                    AS avg_runs,
           AVG(strike_rate)                    AS avg_sr,
           COUNT(*)                            AS innings_count
    FROM   innings
    WHERE  match_date IS NOT NULL
    GROUP  BY player_id, quarter
    HAVING COUNT(*) >= 2
),
trend AS (
    SELECT player_id,
           COUNT(DISTINCT quarter)                    AS quarters,
           MAX(avg_runs)                              AS peak_avg,
           MIN(avg_runs)                              AS trough_avg,
           AVG(CASE WHEN quarter >= (
                      SELECT quarter FROM quarterly q2
                      WHERE q2.player_id = quarterly.player_id
                      ORDER BY quarter DESC LIMIT 1 OFFSET 1
                    ) THEN avg_runs END)              AS recent_avg,
           AVG(CASE WHEN quarter < (
                      SELECT quarter FROM quarterly q3
                      WHERE q3.player_id = quarterly.player_id
                      ORDER BY quarter DESC LIMIT 1
                    ) THEN avg_runs END)              AS earlier_avg
    FROM   quarterly
    GROUP  BY player_id
    HAVING COUNT(DISTINCT quarter) >= 2
)
SELECT p.full_name                      AS "Player",
       t.team_name                      AS "Country",
       tr.quarters                      AS "Quarters Active",
       ROUND(tr.peak_avg, 2)            AS "Peak Avg",
       ROUND(tr.trough_avg, 2)          AS "Trough Avg",
       ROUND(COALESCE(tr.recent_avg,0), 2)  AS "Recent Avg",
       ROUND(COALESCE(tr.earlier_avg,0),2)  AS "Earlier Avg",
       CASE
         WHEN COALESCE(tr.recent_avg,0) > COALESCE(tr.earlier_avg,0) * 1.1
              THEN 'Career Ascending'
         WHEN COALESCE(tr.recent_avg,0) < COALESCE(tr.earlier_avg,0) * 0.9
              THEN 'Career Declining'
         ELSE      'Career Stable'
       END                               AS "Career Phase"
FROM   trend tr
JOIN   players p ON tr.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
ORDER  BY tr.quarters DESC, tr.peak_avg DESC;
""",
    },
}

# PAGE LAYOUT
st.markdown("""
<div style="background:linear-gradient(90deg,#1a1a2e,#0f3460);
            border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;
            border:1px solid #0f3460">
    <span style="font-size:1.8rem;font-weight:800;color:#e2e8f0">🔍 SQL Analytics</span>
    <span style="color:#8b949e;margin-left:1rem">
        25 interactive SQL queries — Beginner → Advanced
    </span>
</div>
""", unsafe_allow_html=True)

# Sidebar query browser + custom SQL
with st.sidebar:
    st.markdown("### 🔍 Query Browser")
    level_filter = st.radio("Level", ["All", "Beginner", "Intermediate", "Advanced"])
    st.markdown("---")

tab_queries, tab_custom = st.tabs(["📋 25 Practice Queries", "⌨️ Custom SQL Editor"])

# TAB 1 — 25 QUERIES
with tab_queries:
    level_colors = {
        "Beginner":     ("#1a3a1a", "#3fb950"),
        "Intermediate": ("#3a2e00", "#f6ad55"),
        "Advanced":     ("#3a1a1a", "#fc8181"),
    }

    for q_name, q_data in QUERIES.items():
        level = q_data["level"]
        if level_filter != "All" and level != level_filter:
            continue

        bg, fg = level_colors[level]
        with st.expander(f"{q_name}  ·  {level}", expanded=False):
            col_info, col_run = st.columns([5, 1])
            with col_info:
                st.markdown(f"""
                <div style="background:{bg};border-left:4px solid {fg};
                            border-radius:6px;padding:0.6rem 0.8rem;margin-bottom:0.5rem">
                    <span style="color:{fg};font-weight:700;font-size:0.8rem">{level.upper()}</span>
                    <div style="color:#c9d1d9;font-size:0.9rem;margin-top:0.2rem">
                        {q_data['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_run:
                run_btn = st.button("▶ Run", key=f"run_{q_name}", use_container_width=True)

            with st.expander("🔎 View SQL", expanded=False):
                st.code(q_data["sql"].strip(), language="sql")

            if run_btn:
                with st.spinner("Running query..."):
                    # Use bridge function
                    results = utils.run_query(q_data["sql"])
                if results:
                    df = pd.DataFrame(results)
                    st.success(f"{len(df)} rows returned")
                    st.dataframe(df, use_container_width=True, hide_index=True)

                    # Auto-chart for specific queries
                    numeric_cols = df.select_dtypes(include="number").columns.tolist()
                    if len(df) > 1 and len(numeric_cols) >= 1:
                        try:
                            first_text = df.select_dtypes(include="object").columns[0]
                            first_num  = numeric_cols[0]
                            if len(df) <= 25:
                                fig = px.bar(
                                    df.head(15),
                                    x=first_text, y=first_num,
                                    title=f"{q_name} — {first_num}",
                                    color_discrete_sequence=["#58a6ff"],
                                )
                                fig.update_layout(**_PLOTLY_LAYOUT)
                                fig.update_xaxes(tickangle=-30)
                                st.plotly_chart(fig, use_container_width=True)
                        except (Exception):
                            pass

                    # CSV download
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "⬇️ Download CSV",
                        data=csv,
                        file_name=f"{q_name.replace(' ','_')}.csv",
                        mime="text/csv",
                        key=f"dl_{q_name}",
                    )
                else:
                    st.warning("Query returned no results. Check seed data or query conditions.")

# TAB 2 — CUSTOM SQL EDITOR
with tab_custom:
    st.markdown('<div class="section-title">⌨️ Custom SQL Editor</div>',
                unsafe_allow_html=True)

    st.info("Write any SELECT query against the cricket database. "
            "INSERT / UPDATE / DELETE are disabled for safety.")

    default_sql = """-- Example: Top 5 players by ODI runs
SELECT p.full_name AS Player,
       t.team_name AS Country,
       bs.runs_scored AS Runs,
       bs.batting_avg AS Average
FROM   batting_stats bs
JOIN   players p ON bs.player_id = p.player_id
JOIN   teams   t ON p.team_id    = t.team_id
WHERE  bs.format = 'ODI'
ORDER  BY bs.runs_scored DESC
LIMIT  5;"""

    custom_sql = st.text_area(
        "Your SQL query", value=default_sql, height=220,
        key="custom_sql_input",
    )

    col_exec, col_clear, col_schema = st.columns([1, 1, 3])
    with col_exec:
        exec_btn = st.button("▶ Execute", use_container_width=True, type="primary")
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()
    with col_schema:
        st.caption("Available tables: teams, venues, series, matches, players, "
                   "batting_stats, bowling_stats, innings, bowling_innings, fielding_stats")

    if exec_btn:
        sql_lower = custom_sql.strip().lower()
        if any(kw in sql_lower for kw in ["insert", "update", "delete", "drop", "alter", "create"]):
            st.error("Only SELECT queries are allowed in this editor.")
        elif not sql_lower.startswith("select") and not sql_lower.startswith("with"):
            st.error("Query must start with SELECT or WITH.")
        else:
            with st.spinner("Executing..."):
                # Use bridge function
                results = utils.run_query(custom_sql)
            if results:
                df = pd.DataFrame(results)
                st.success(f"✅ {len(df)} rows returned")
                st.dataframe(df, use_container_width=True, hide_index=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    "⬇️ Download CSV", data=csv,
                    file_name="custom_query.csv", mime="text/csv",
                )
            else:
                st.warning("No results returned.")

    # Schema reference
    with st.expander("📖 Full Database Schema Reference"):
        schema_info = {
            "players":        "player_id, full_name, team_id, playing_role, batting_style, bowling_style, nationality, date_of_birth",
            "teams":          "team_id, team_name, country, format",
            "matches":        "match_id, match_desc, team1_id, team2_id, venue_id, series_id, match_date, match_format, toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type, status",
            "venues":         "venue_id, venue_name, city, country, capacity",
            "series":         "series_id, series_name, host_country, match_type, start_date, end_date, total_matches",
            "batting_stats":  "stat_id, player_id, format, matches, innings, runs_scored, highest_score, batting_avg, strike_rate, centuries, half_centuries",
            "bowling_stats":  "stat_id, player_id, format, matches, innings, overs_bowled, wickets_taken, runs_conceded, bowling_avg, economy_rate, best_bowling, five_wickets",
            "innings":        "innings_id, match_id, player_id, innings_number, batting_position, runs_scored, balls_faced, strike_rate, fours, sixes, dismissed, match_date",
            "bowling_innings":"bowling_innings_id, match_id, player_id, innings_number, overs_bowled, maidens, runs_conceded, wickets_taken, economy_rate, match_date",
            "fielding_stats": "stat_id, player_id, catches, stumpings, run_outs",
        }
        for table, cols in schema_info.items():
            st.markdown(f"**`{table}`** — `{cols}`")

# Footer
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#484f58;font-size:0.8rem;
            border-top:1px solid #21262d;padding-top:1rem">
    🔍 25 SQL queries | Beginner → Intermediate → Advanced
    &nbsp;|&nbsp; Custom editor with schema reference
</div>
""", unsafe_allow_html=True)