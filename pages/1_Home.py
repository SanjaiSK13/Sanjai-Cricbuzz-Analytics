import streamlit as st
from pathlib import Path
from utils.db_connection import init_db, get_dashboard_stats

# Page config
st.set_page_config(
    page_title="Home | Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS
css_path = Path(__file__).resolve().parent.parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Bootstrap DB
@st.cache_resource
def _init():
    init_db()
    return True
_init()

# HERO BANNER
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0d1117 0%, #1a1a2e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    border: 1px solid #0f3460;
">
    <div class="hero-title">🏏 Cricbuzz LiveStats</div>
    <div class="hero-subtitle">
        A comprehensive cricket analytics dashboard — live scores, player stats,
        SQL-driven insights &amp; full data management in one place.
    </div>
    <br/>
    <span class="tool-pill">🐍 Python</span>
    <span class="tool-pill">⚡ Streamlit</span>
    <span class="tool-pill">🗄️ SQLite</span>
    <span class="tool-pill">🌐 Cricbuzz API</span>
    <span class="tool-pill">🐼 Pandas</span>
    <span class="tool-pill">📊 Plotly</span>
    <span class="tool-pill">🔗 RapidAPI</span>
</div>
""", unsafe_allow_html=True)

# LIVE SUMMARY CARDS
st.markdown('<div class="section-title">📊 Database Overview</div>', unsafe_allow_html=True)

try:
    stats = get_dashboard_stats()
    # Fallback if the function returns None or is empty
    if not stats:
        stats = {}
except Exception:
    stats = {}

# Use .get() with default 0 to prevent KeyError: 'total_players'
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("🏏 Players",       stats.get("total_players", 0))
c2.metric("📅 Matches",       stats.get("total_matches", 0))
c3.metric("🌍 Teams",         stats.get("total_teams", 0))
c4.metric("🏟️ Venues",        stats.get("total_venues", 0))
c5.metric("🔴 Live Now",      stats.get("live_matches", 0))
c6.metric("⏳ Upcoming",      stats.get("upcoming", 0))

st.markdown("<br/>", unsafe_allow_html=True)

# PAGE GUIDE
st.markdown('<div class="section-title">🗺️ Pages Guide</div>', unsafe_allow_html=True)

pages = [
    ("📺", "Live Matches",     "pages/2_Live_Matches.py",
     "Real-time scorecards from the Cricbuzz API. See live scores, batting & bowling innings, current partnerships, and upcoming fixtures. Refreshes on demand."),
    ("📊", "Player Stats",     "pages/3_Player_Stats.py",
     "Top batting and bowling rankings from the Cricbuzz API. Filter by format (Test / ODI / T20I), browse career stats, and visualise performance with Plotly charts."),
    ("🔍", "SQL Analytics",    "pages/4_SQL_Analytics.py",
     "25 hand-crafted SQL queries across Beginner → Intermediate → Advanced levels. Run any query interactively, view tabular results, and explore the underlying SQL."),
    ("🛠️", "CRUD Operations", "pages/5_CRUD_Operations.py",
     "Full Create / Read / Update / Delete operations on Players, Matches, Venues, and Stats via form-based UI. Great for learning database manipulation."),
]

col_a, col_b = st.columns(2)
for i, (icon, title, _path, desc) in enumerate(pages):
    col = col_a if i % 2 == 0 else col_b
    with col:
        st.markdown(f"""
        <div class="stat-card" style="min-height:110px">
            <div style="font-size:1.4rem;font-weight:700;color:#58a6ff;margin-bottom:0.3rem">
                {icon} {title}
            </div>
            <div style="color:#8b949e;font-size:0.88rem;line-height:1.5">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# PROJECT STRUCTURE
st.markdown('<div class="section-title">📁 Project Structure</div>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.code("""
cricbuzz_livestats/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env                     # API key & DB path
├── .env.example             # Safe template
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   ├── db_connection.py     # SQLite helpers + CRUD
│   └── api_helper.py        # Cricbuzz API wrapper
│
├── pages/
│   ├── 1_Home.py            # This page
│   ├── 2_Live_Matches.py    # Live scorecard
│   ├── 3_Player_Stats.py    # Rankings & charts
│   ├── 4_SQL_Analytics.py   # 25 SQL queries
│   └── 5_CRUD_Operations.py # Data management
│
├── database/
│   ├── schema.sql           # 10 table definitions
│   ├── seed_data.sql        # Sample data
│   └── cricket.db           # Auto-generated SQLite
│
└── assets/
    └── style.css            # Custom theme
""", language="text")

with col_right:
    st.markdown("**Database Schema (10 tables)**")
    tables = [
        ("teams",          "20 rows",  "International cricket teams"),
        ("venues",         "15 rows",  "Stadiums with capacity"),
        ("series",         "12 rows",  "Tournament & series info"),
        ("matches",        "35 rows",  "Results, toss, venue, winner"),
        ("players",        "40 rows",  "Profiles, roles, styles"),
        ("batting_stats",  "55 rows",  "Career aggregates by format"),
        ("bowling_stats",  "40 rows",  "Career aggregates by format"),
        ("innings",        "60 rows",  "Per-innings batting scores"),
        ("bowling_innings","44 rows",  "Per-innings bowling figures"),
        ("fielding_stats", "35 rows",  "Catches, stumpings, run-outs"),
    ]
    for name, count, desc in tables:
        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:5px 0;
                    border-bottom:1px solid #1f2937">
            <span style="color:#58a6ff;font-family:monospace;
                         font-size:0.85rem;width:180px">{name}</span>
            <span style="color:#3fb950;font-size:0.8rem;width:70px">{count}</span>
            <span style="color:#8b949e;font-size:0.8rem">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# QUICK START GUIDE
st.markdown('<div class="section-title">🚀 Quick Start Guide</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**1. Install dependencies**")
    st.code("pip install -r requirements.txt", language="bash")

    st.markdown("**2. Configure your API key**")
    st.code("""# .env
RAPIDAPI_KEY=your_key_here
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
DB_PATH=database/cricket.db""", language="bash")

    st.markdown("**3. Run the app**")
    st.code("streamlit run main.py", language="bash")

with col2:
    st.markdown("**4. Get your RapidAPI key**")
    st.info("""
1. Visit [rapidapi.com](https://rapidapi.com)
2. Search **"Cricbuzz Cricket API"**
3. Subscribe → **Basic (Free)** plan
4. Copy your **X-RapidAPI-Key**
5. Paste into `.env` file
    """)
    st.markdown("**5. Tech stack versions**")
    deps = {
        "Python":     "3.10+",
        "Streamlit":  "1.32+",
        "Pandas":     "2.0+",
        "Plotly":     "5.18+",
        "Requests":   "2.31+",
        "python-dotenv": "1.0+",
    }
    for lib, ver in deps.items():
        st.markdown(f"- `{lib}` ≥ {ver}")

# SQL QUERIES PREVIEW
st.markdown('<div class="section-title">🧮 SQL Analytics Preview (25 Queries)</div>',
            unsafe_allow_html=True)

tab_b, tab_i, tab_a = st.tabs(["🟢 Beginner (Q1–8)", "🟡 Intermediate (Q9–16)", "🔴 Advanced (Q17–25)"])

with tab_b:
    queries = [
        ("Q1", "Indian Players",       "All players representing India with roles & styles"),
        ("Q2", "Recent Matches",       "Matches played in the last few days, sorted by date"),
        ("Q3", "Top ODI Run Scorers",  "Top 10 highest run scorers in ODI cricket"),
        ("Q4", "Large Venues",         "Venues with capacity > 25,000 sorted by size"),
        ("Q5", "Team Win Counts",      "Total wins per team across all formats"),
        ("Q6", "Players by Role",      "Count of Batsmen, Bowlers, All-rounders, WK"),
        ("Q7", "Highest Scores",       "Highest individual batting score per format"),
        ("Q8", "2024 Series",          "All series that started in 2024"),
    ]
    for qnum, qtitle, qdesc in queries:
        st.markdown(f"**`{qnum}`** {qtitle} — <span style='color:#8b949e'>{qdesc}</span>",
                    unsafe_allow_html=True)

with tab_i:
    queries = [
        ("Q9",  "All-rounder Greats",    "1000+ runs AND 50+ wickets in career"),
        ("Q10", "Last 20 Results",       "Completed matches with winner & victory type"),
        ("Q11", "Cross-format Stats",    "Player runs across Test / ODI / T20I formats"),
        ("Q12", "Home vs Away",          "Each team's win record at home vs away"),
        ("Q13", "100+ Partnerships",     "Batting pairs with combined 100+ runs"),
        ("Q14", "Venue Bowling",         "Economy & wickets per bowler per venue"),
        ("Q15", "Close Match Heroes",    "Players who perform in matches decided by <50 runs/<5 wkts"),
        ("Q16", "Year-on-year Form",     "Average runs & SR per player per year since 2020"),
    ]
    for qnum, qtitle, qdesc in queries:
        st.markdown(f"**`{qnum}`** {qtitle} — <span style='color:#8b949e'>{qdesc}</span>",
                    unsafe_allow_html=True)

with tab_a:
    queries = [
        ("Q17", "Toss Advantage",        "Win% for toss winners broken down by bat/bowl decision"),
        ("Q18", "Economical Bowlers",    "Best economy in ODI & T20I (min 10 matches, 2 ov/match)"),
        ("Q19", "Batting Consistency",   "Std deviation of scores — lower = more consistent"),
        ("Q20", "Format Participation",  "Match count & avg per player per format (min 20 total)"),
        ("Q21", "Performance Ranking",   "Weighted batting + bowling + fielding composite score"),
        ("Q22", "Head-to-Head",          "Win% & avg margin for team pairs (min 5 matches, 3 yrs)"),
        ("Q23", "Form Analysis",         "Last 10 innings → Excellent / Good / Average / Poor Form"),
        ("Q24", "Best Partnerships",     "Top batting pairs by avg partnership (min 5 together)"),
        ("Q25", "Career Trajectory",     "Quarterly performance trend → Ascending / Declining / Stable"),
    ]
    for qnum, qtitle, qdesc in queries:
        st.markdown(f"**`{qnum}`** {qtitle} — <span style='color:#8b949e'>{qdesc}</span>",
                    unsafe_allow_html=True)

# Footer
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#484f58;font-size:0.8rem;
            border-top:1px solid #21262d;padding-top:1rem">
    🏏 Cricbuzz LiveStats &nbsp;|&nbsp; Built with Streamlit + SQLite + Cricbuzz API
    &nbsp;|&nbsp; Data for educational purposes
</div>
""", unsafe_allow_html=True)