import streamlit as st
import pandas as pd
from pathlib import Path
import utils  # Use the synchronized bridge

# Page config
st.set_page_config(
    page_title="Live Matches | Cricbuzz LiveStats",
    page_icon="📺",
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

# Helpers
def _fmt_badge(status: str) -> str:
    if status == "live":
        return '<span class="live-badge">🔴 LIVE</span>'
    if status == "upcoming":
        return '<span class="upcoming-badge">⏳ UPCOMING</span>'
    return '<span class="completed-badge">✅ COMPLETED</span>'


def _scorecard_section(card: dict) -> None:
    hdr = card.get("match_header", {})
    if hdr.get("status"):
        st.markdown(f"""
        <div style="background:#161b22;border:1px solid #0f3460;border-radius:10px;
                    padding:1rem;margin-bottom:1rem">
            <span style="color:#58a6ff;font-weight:700">Status: </span>
            <span style="color:#e2e8f0">{hdr['status']}</span>
            {"&nbsp; &nbsp; <span style='color:#6b7280'>Toss: "+hdr['toss']+" elected to "+hdr['toss_decision']+"</span>" if hdr.get('toss') else ""}
        </div>
        """, unsafe_allow_html=True)

    for innings in card.get("innings", []):
        team_name = innings.get('team_name', innings.get('title', 'Team'))
        score = innings.get('score', innings.get('total', {}).get('runs', 0))
        wickets = innings.get('wickets', innings.get('total', {}).get('wickets', 0))
        overs = innings.get('overs', innings.get('total', {}).get('overs', 0))
        
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin:1rem 0 0.4rem">
            <span style="font-size:1.1rem;font-weight:700;color:#e2e8f0">
                {team_name} Innings
            </span>
            <span style="font-size:1.4rem;font-weight:800;color:#58a6ff">
                {score}/{wickets}
            </span>
            <span style="color:#8b949e">({overs} ov)</span>
        </div>
        """, unsafe_allow_html=True)

        col_bat, col_bowl = st.columns(2)
        with col_bat:
            st.markdown("**Batting**")
            if innings.get("batsmen"):
                df_bat = pd.DataFrame(innings["batsmen"])
                df_bat.columns = [c.upper() for c in df_bat.columns]
                st.dataframe(df_bat, use_container_width=True, hide_index=True)
        with col_bowl:
            st.markdown("**Bowling**")
            if innings.get("bowlers"):
                df_bowl = pd.DataFrame(innings["bowlers"])
                df_bowl.columns = [c.upper() for c in df_bowl.columns]
                st.dataframe(df_bowl, use_container_width=True, hide_index=True)
        st.markdown("---")

# PAGE HEADER
st.markdown("""
<div style="background:linear-gradient(90deg,#1a1a2e,#0f3460);
            border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;
            border:1px solid #0f3460">
    <span style="font-size:1.8rem;font-weight:800;color:#e2e8f0">📺 Live Matches</span>
    <span style="color:#8b949e;margin-left:1rem">
        Real-time scorecards powered by the Cricbuzz API
    </span>
</div>
""", unsafe_allow_html=True)

# Refresh control
col_refresh, col_info = st.columns([1, 5])
with col_refresh:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
with col_info:
    st.caption("Data fetched live from Cricbuzz API. Falls back to mock data if key is not set.")

st.markdown("---")

# TABS
tab_live, tab_upcoming, tab_recent, tab_series = st.tabs([
    "🔴 Live Now", "⏳ Upcoming", "✅ Recent Results", "📋 Active Series"
])

# TAB 1 — LIVE NOW
with tab_live:
    st.markdown('<div class="section-title">🔴 Matches in Progress</div>',
                unsafe_allow_html=True)

    with st.spinner("Fetching live matches..."):
        live_matches = utils.get_live_matches()

    if not live_matches:
        st.info("No live matches at the moment. Check back soon!")
    else:
        for match in live_matches:
            t1_score = match.get('team1_score', match.get('score_team1', '0/0 (0 ov)'))
            t2_score = match.get('team2_score', match.get('score_team2', '0/0 (0 ov)'))
            
            with st.expander(
                f"🏏 {match['team1_name']} vs {match['team2_name']} — {match['description']} "
                f"| {match['match_format']}",
                expanded=True,
            ):
                # Match meta
                col_a, col_b, col_c = st.columns(3)
                col_a.markdown(f"**🏟️ Venue:** {match['venue_name']}, {match['venue_city']}")
                col_b.markdown(f"**🏆 Series:** {match.get('series_name','–')}")
                col_c.markdown(f"**📋 Format:** {match['match_format']}")

                # Scores
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown(f"""
                    <div class="stat-card" style="text-align:center">
                        <div style="font-size:1rem;color:#8b949e">{match['team1_name']}</div>
                        <div style="font-size:2rem;font-weight:800;color:#58a6ff">
                            {t1_score}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with sc2:
                    st.markdown(f"""
                    <div class="stat-card" style="text-align:center">
                        <div style="font-size:1rem;color:#8b949e">{match['team2_name']}</div>
                        <div style="font-size:2rem;font-weight:800;color:#f6ad55">
                            {t2_score}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Status
                st.markdown(f"""
                <div style="text-align:center;margin-top:0.5rem;font-size:1rem;
                            color:#68d391;font-weight:600">
                    {match['status']}
                </div>
                """, unsafe_allow_html=True)

                # Detailed scorecard
                st.markdown("##### Detailed Scorecard")
                if st.button(f"Load Scorecard: {match['team1_short']} vs {match['team2_short']}", key=str(match['match_id'])):
                    with st.spinner("Loading scorecard..."):
                        card = utils.get_match_scorecard(str(match["match_id"]))
                    _scorecard_section(card)

# TAB 2 — UPCOMING
with tab_upcoming:
    st.markdown('<div class="section-title">⏳ Upcoming Fixtures</div>',
                unsafe_allow_html=True)

    col_src1, col_src2 = st.columns(2)

    # API upcoming
    with col_src1:
        st.markdown("**From Cricbuzz API**")
        with st.spinner("Fetching upcoming matches..."):
            upcoming_api = utils.get_upcoming_matches()

        for m in upcoming_api:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-weight:700;color:#e2e8f0">
                    {m['team1_name']} vs {m['team2_name']}
                </div>
                <div style="color:#8b949e;font-size:0.85rem">
                    {m['description']} &nbsp;|&nbsp; {m['match_format']}
                </div>
                <div style="color:#6b7280;font-size:0.82rem;margin-top:0.2rem">
                    🏟️ {m['venue_name']}, {m['venue_city']} &nbsp;|&nbsp; 🕐 {m['start_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # DB upcoming
    with col_src2:
        st.markdown("**From Local Database**")
        db_upcoming = utils.get_all_matches(status="upcoming")
        for m in db_upcoming:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-weight:700;color:#e2e8f0">
                    {m['team1']} vs {m['team2']}
                </div>
                <div style="color:#8b949e;font-size:0.85rem">
                    {m['match_desc']} &nbsp;|&nbsp; {m['match_format']}
                </div>
                <div style="color:#6b7280;font-size:0.82rem;margin-top:0.2rem">
                    🏟️ {m['venue_name']}, {m['city']} &nbsp;|&nbsp; 📅 {m['match_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# TAB 3 — RECENT RESULTS
with tab_recent:
    st.markdown('<div class="section-title">✅ Recent Results</div>',
                unsafe_allow_html=True)

    col_filter1, col_filter2, _ = st.columns([2, 2, 4])
    with col_filter1:
        fmt_filter = st.selectbox("Format", ["All", "Test", "ODI", "T20I"])
    with col_filter2:
        limit = st.selectbox("Show last", [10, 20, 30, 50], index=1)

    completed = utils.get_all_matches(status="completed")

    if fmt_filter != "All":
        completed = [m for m in completed if m.get("match_format") == fmt_filter]
    completed = completed[:limit]

    if not completed:
        st.info("No completed matches found.")
    else:
        for m in completed:
            winner_text = f"🏆 {m['winner']} won by {m['victory_margin']} {m['victory_type']}" \
                          if m.get("winner") else "No result"
            st.markdown(f"""
            <div class="stat-card" style="margin-bottom:0.5rem">
                <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                        <span style="font-weight:700;color:#e2e8f0">
                            {m['team1']} vs {m['team2']}
                        </span>
                        <span style="color:#8b949e;font-size:0.82rem;margin-left:8px">
                            {m['match_desc']}
                        </span>
                        <span style="background:#1f2937;border-radius:4px;padding:1px 6px;
                                     font-size:0.75rem;color:#9ca3af;margin-left:6px">
                            {m['match_format']}
                        </span>
                    </div>
                    <span style="color:#8b949e;font-size:0.82rem">{m['match_date']}</span>
                </div>
                <div style="margin-top:0.3rem">
                    <span style="color:#68d391;font-size:0.88rem">{winner_text}</span>
                    <span style="color:#484f58;font-size:0.8rem;margin-left:8px">
                        🏟️ {m['venue_name']}, {m['city']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Summary dataframe
        st.markdown("##### Summary Table")
        df_results = pd.DataFrame([{
            "Match":    f"{m['team1']} vs {m['team2']}",
            "Format":   m["match_format"],
            "Date":     m["match_date"],
            "Winner":   m.get("winner", "–"),
            "Margin":   f"{m.get('victory_margin','–')} {m.get('victory_type','')}" if m.get("winner") else "–",
            "Venue":    f"{m['venue_name']}, {m['city']}",
        } for m in completed])
        st.dataframe(df_results, use_container_width=True, hide_index=True)

# TAB 4 — ACTIVE SERIES
with tab_series:
    st.markdown('<div class="section-title">📋 Active & Recent Series</div>',
                unsafe_allow_html=True)

    col_api_s, col_db_s = st.columns(2)

    with col_api_s:
        st.markdown("**Cricbuzz API — Current Series**")
        with st.spinner("Loading series..."):
            series_list = utils.get_current_series()
        for s in series_list:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-weight:700;color:#e2e8f0">{s['name']}</div>
                <div style="color:#8b949e;font-size:0.82rem;margin-top:0.2rem">
                    📅 {s.get('start_date','–')} → {s.get('end_date','–')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_db_s:
        st.markdown("**Database — All Series**")
        db_series = utils.run_query(
            "SELECT series_name, host_country, match_type, start_date, "
            "end_date, total_matches FROM series ORDER BY start_date DESC"
        )
        if db_series:
            df_series = pd.DataFrame(db_series)
            df_series.columns = ["Series", "Host", "Type", "Start", "End", "Matches"]
            st.dataframe(df_series, use_container_width=True, hide_index=True)

# Footer
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#484f58;font-size:0.8rem;
            border-top:1px solid #21262d;padding-top:1rem">
    Stat: OK | 📺 Live data from Cricbuzz API via RapidAPI &nbsp;|&nbsp;
    Mock data shown when API key is not configured
</div>
""", unsafe_allow_html=True)