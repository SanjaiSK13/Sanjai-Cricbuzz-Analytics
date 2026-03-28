# 🏏 Cricbuzz LiveStats — Cricket Analytics Dashboard

An end-to-end **Cricket Analytics Platform** that integrates live data from the **Cricbuzz API** with a relational SQLite database to deliver real-time match intelligence, player statistics, SQL-driven analytics, and full data management — all through an interactive multi-page Streamlit dashboard.

---

## Overview

Cricbuzz LiveStats bridges the gap between raw cricket data and actionable insight. Instead of simply displaying scores, the platform answers the questions analysts, fans, and fantasy players ask every day:

- _Who are the most consistent batsmen right now?_
- _Which teams perform better at home vs away?_
- _What is the toss advantage across formats?_
- _Who are the best bowling partners at each venue?_

By combining **live Cricbuzz API data** with a **structured SQLite database** and **25 hand-crafted SQL analytics queries**, the platform surfaces patterns across players, matches, venues, and formats — presented through a production-ready dashboard with full CRUD data management.

---

## Key Capabilities

- Real-time live match scorecards from the Cricbuzz API via RapidAPI
- Top batting and bowling ICC rankings across Test, ODI, and T20I formats
- SQLite database with 10 tables, 40 players, 35 matches, and 15 venues seeded
- 25 SQL analytics queries from beginner SELECT to advanced window functions and CTEs
- Interactive custom SQL editor with schema reference
- Full CRUD operations on Players, Matches, Venues, and Career Stats
- Plotly charts — scatter, bar, pie, and bubble visualisations
- Automatic mock data fallback when API key is not configured
- Database health checks and audit log built in

---

## Tech Stack

### Core

- Python 3.10+
- Streamlit 1.32+
- SQLite (via `sqlite3` standard library)
- python-dotenv

### Data & Analytics

- Pandas 2.0+
- NumPy 1.26+
- Requests 2.31+

### Visualisation

- Plotly 5.18+ — interactive charts
- Altair 5.2+

### API

- Cricbuzz Cricket API via RapidAPI
- REST / JSON — live matches, rankings, scorecards, series

---

## System Architecture

```
Cricbuzz API (RapidAPI)
        ↓
  utils/api_helper.py          ← REST wrapper + mock fallback
        ↓
  utils/__init__.py             ← Unified interface layer
        ↓
  utils/db_connection.py        ← SQLite connection + query runner
        ↓
  database/cricket.db           ← 10-table relational schema
  database/schema.sql           ← Table definitions + indexes
  database/seed_data.sql        ← 40 players, 35 matches, seed data
        ↓
  pages/
  ├── 1_Home.py                 ← Overview + live summary cards
  ├── 2_Live_Matches.py         ← Real-time scorecards
  ├── 3_Player_Stats.py         ← Rankings + career charts
  ├── 4_SQL_Analytics.py        ← 25 interactive SQL queries
  └── 5_CRUD_Operations.py      ← Data management UI
        ↓
  Streamlit Cloud Deployment
```

---

## Project Structure

```
cricbuzz_livestats/
│
├── main.py                      ← Entry point — navigation & DB bootstrap
├── requirements.txt             ← All pip dependencies
├── .env                         ← API key & DB path (never committed)
├── .env.example                 ← Safe template to share
├── .gitignore
│
├── utils/
│   ├── __init__.py              ← Unified interface for all pages
│   ├── db_connection.py         ← SQLite helpers, CRUD, query runner
│   └── api_helper.py            ← Cricbuzz API wrapper + mock data
│
├── pages/
│   ├── 1_Home.py                ← Hero, stats cards, project guide
│   ├── 2_Live_Matches.py        ← Live scores, upcoming, results, series
│   ├── 3_Player_Stats.py        ← API rankings, DB career stats, charts
│   ├── 4_SQL_Analytics.py       ← 25 SQL queries + custom editor
│   └── 5_CRUD_Operations.py     ← Players / Matches / Venues / Stats CRUD
│
├── database/
│   ├── schema.sql               ← 10 table definitions + 16 indexes
│   ├── seed_data.sql            ← Sample data for all 10 tables
│   └── cricket.db               ← Auto-generated SQLite file (git-ignored)
│
└── assets/
    └── style.css                ← Custom Streamlit dark theme
```

---

## Database Schema (10 Tables)

| Table             | Rows (seed) | Description                             |
| ----------------- | ----------- | --------------------------------------- |
| `teams`           | 20          | International cricket teams             |
| `venues`          | 15          | Stadiums with city, country, capacity   |
| `series`          | 12          | Tournament and series metadata          |
| `matches`         | 35          | Results, toss, venue, winner, format    |
| `players`         | 40          | Profiles, roles, batting/bowling styles |
| `batting_stats`   | 55          | Career aggregates per player per format |
| `bowling_stats`   | 40          | Career aggregates per player per format |
| `innings`         | 60          | Per-innings batting scores and details  |
| `bowling_innings` | 44          | Per-innings bowling figures             |
| `fielding_stats`  | 35          | Catches, stumpings, run-outs            |

---

## SQL Analytics — 25 Queries

### 🟢 Beginner (Q1–Q8)

| #   | Query                           | Concepts                    |
| --- | ------------------------------- | --------------------------- |
| Q1  | All players representing India  | SELECT, JOIN, WHERE         |
| Q2  | Recent matches in last 180 days | WHERE with date(), ORDER BY |
| Q3  | Top 10 ODI run scorers          | ORDER BY, LIMIT             |
| Q4  | Venues with capacity > 25,000   | WHERE, ORDER BY             |
| Q5  | Team win counts                 | GROUP BY, COUNT, JOIN       |
| Q6  | Players by playing role         | GROUP BY, COUNT             |
| Q7  | Highest score per format        | MAX, GROUP BY               |
| Q8  | Series starting in 2024         | strftime(), WHERE           |

### 🟡 Intermediate (Q9–Q16)

| #   | Query                                       | Concepts                  |
| --- | ------------------------------------------- | ------------------------- |
| Q9  | All-rounders with 1000+ runs & 50+ wickets  | Multi-table JOIN, HAVING  |
| Q10 | Last 20 completed match results             | Subquery, ORDER BY, LIMIT |
| Q11 | Cross-format batting comparison             | CASE WHEN pivot, HAVING   |
| Q12 | Home vs away team performance               | Conditional aggregation   |
| Q13 | 100+ batting partnerships                   | Self-JOIN on innings      |
| Q14 | Bowling performance per venue               | GROUP BY multi-column     |
| Q15 | Close match heroes (<50 runs or <5 wickets) | Complex WHERE, AVG        |
| Q16 | Year-on-year batting form since 2020        | strftime(), GROUP BY year |

### 🔴 Advanced (Q17–Q25)

| #   | Query                                      | Concepts                       |
| --- | ------------------------------------------ | ------------------------------ |
| Q17 | Toss advantage win percentage              | CASE WHEN, ROUND, percentage   |
| Q18 | Most economical bowlers in limited overs   | Multi-condition HAVING         |
| Q19 | Batting consistency via standard deviation | Manual STDDEV with SQL math    |
| Q20 | Multi-format participation matrix          | CASE WHEN pivot, SUM           |
| Q21 | Weighted performance ranking system        | CTE, window RANK()             |
| Q22 | Head-to-head team analysis                 | CTE, self-JOIN, win %          |
| Q23 | Player form categorisation                 | CTE, ROW_NUMBER(), CASE        |
| Q24 | Best batting partnership pairs             | Self-JOIN, COUNT, success rate |
| Q25 | Career trajectory time-series              | CTE, quarterly grouping, trend |

---

## Dashboard Pages

### 🏠 Home

Executive summary with 6 live database metric cards, page navigation guide, business use case overview, full database schema reference, quick-start instructions, and a tabbed SQL query preview.

### 📺 Live Matches

Real-time live scorecard with batting and bowling innings tables. Upcoming fixtures from both Cricbuzz API and local database. Recent results with format filter and summary table. Active series from API and database.

### 📊 Player Stats

Top batting and bowling ICC rankings from the Cricbuzz API with medal display and rating bar charts. Database career stats per player across all formats with Plotly scatter and bar charts. Player search across database and Cricbuzz API. Role distribution pie chart.

### 🔍 SQL Analytics

All 25 queries browsable by level (Beginner / Intermediate / Advanced). Each query has a description, expandable SQL view, Run button, results dataframe, auto-generated bar chart, and CSV download. Custom SQL editor with safety guards and full schema reference.

### 🛠️ CRUD Operations

Form-based Create, Read, Update, Delete for Players, Matches, Venues, and Batting/Bowling Stats. Confirmation checkboxes for destructive operations. Audit log showing recently added records. Database health check for orphaned records and referential integrity.

---

## API Integration

| Function                  | Endpoint                     | Fallback            |
| ------------------------- | ---------------------------- | ------------------- |
| `get_live_matches()`      | `/matches/v1/live`           | ✅ Mock scorecard   |
| `get_upcoming_matches()`  | `/matches/v1/upcoming`       | ✅ Mock fixtures    |
| `get_match_scorecard()`   | `/mcenter/v1/{id}/scard`     | ✅ Mock innings     |
| `get_top_batting_stats()` | `/stats/v1/rankings/batsmen` | ✅ Mock top 10      |
| `get_top_bowling_stats()` | `/stats/v1/rankings/bowlers` | ✅ Mock top 10      |
| `get_current_series()`    | `/series/v1/active`          | ✅ Mock series list |

> All API functions fail gracefully — the entire dashboard is fully functional with mock data when no API key is provided.

---

## Business Use Cases

| Stakeholder                 | Value Delivered                                                                     |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Sports Media & Broadcasting | Real-time match updates, player form analysis, historical trend data for commentary |
| Fantasy Cricket Platforms   | Player form tracking, head-to-head stats, live score updates for leagues            |
| Cricket Analytics Firms     | Advanced statistical modelling, cross-format performance comparison                 |
| Educational Institutions    | SQL practice with real-world data, API integration and web development learning     |
| Sports Betting & Prediction | Venue-specific performance, toss advantage analysis, momentum tracking              |

---

## Installation & Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/cricbuzz-livestats.git
cd cricbuzz-livestats

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
cp .env.example .env
# Open .env and set:
# RAPIDAPI_KEY=your_key_here
# RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
# DB_PATH=database/cricket.db

# 5. Launch the app
streamlit run main.py
```

> The database is created and seeded automatically on first run — no manual SQL steps needed.

---

## Getting a RapidAPI Key

1. Visit [rapidapi.com](https://rapidapi.com) and create a free account
2. Search for **"Cricbuzz Cricket API"**
3. Subscribe to the **Basic (Free)** plan
4. Copy your **X-RapidAPI-Key** from the code snippet panel
5. Paste it into your `.env` file as `RAPIDAPI_KEY`

---

## Deployment on Streamlit Cloud

```
GitHub push → Streamlit Cloud pulls → Redeploys automatically
```

1. Push your code to GitHub (`.env` and `cricket.db` are git-ignored)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set **Main file path** to `main.py`
5. Add secrets under **Advanced settings**:
   ```toml
   RAPIDAPI_KEY = "your_key_here"
   RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
   DB_PATH = "database/cricket.db"
   ```
6. Click **Deploy** — done

---

## Environment Variables

| Variable        | Description                        | Example                           |
| --------------- | ---------------------------------- | --------------------------------- |
| `RAPIDAPI_KEY`  | Your RapidAPI key for Cricbuzz API | `ghp_abc123...`                   |
| `RAPIDAPI_HOST` | RapidAPI host for Cricbuzz         | `cricbuzz-cricket.p.rapidapi.com` |
| `DB_PATH`       | Path to the SQLite database file   | `database/cricket.db`             |
| `DEBUG_MODE`    | Enable verbose logging             | `False`                           |

---

## Author

**Sanjai K**
Domain: Sports Analytics · SQL · Python · Streamlit · API Integration

---

## License

This project is for educational and portfolio purposes.
Cricket data sourced from the Cricbuzz API via RapidAPI.
