import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import utils

# Page config
st.set_page_config(
    page_title="Player Stats | Cricbuzz LiveStats",
    page_icon="📊",
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

# Plotly theme helper
_PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="sans-serif"),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
)

# PAGE HEADER
st.markdown("""
<div style="background:linear-gradient(90deg,#1a1a2e,#0f3460);
            border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;
            border:1px solid #0f3460">
    <span style="font-size:1.8rem;font-weight:800;color:#e2e8f0">📊 Player Statistics</span>
    <span style="color:#8b949e;margin-left:1rem">
        Rankings, career stats, and performance charts
    </span>
</div>
""", unsafe_allow_html=True)

# Format selector (shared across tabs)
fmt_col, _, refresh_col = st.columns([2, 5, 1])
with fmt_col:
    selected_fmt = st.selectbox(
        "Cricket Format", ["ODI", "Test", "T20I"], key="fmt_global"
    )
with refresh_col:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# TABS
tab_bat, tab_bowl, tab_db, tab_search = st.tabs([
    "🏏 Top Batsmen", "🎯 Top Bowlers",
    "📋 DB Career Stats", "🔍 Player Search",
])

# TAB 1 — TOP BATSMEN (API rankings)
with tab_bat:
    st.markdown('<div class="section-title">🏏 Top Batting Rankings (Cricbuzz API)</div>',
                unsafe_allow_html=True)

    with st.spinner(f"Loading {selected_fmt} batting rankings..."):
        bat_data = utils.get_top_batting_stats(selected_fmt)

    if bat_data:
        df_bat = pd.DataFrame(bat_data)
        # Ensure correct column count before renaming
        if len(df_bat.columns) >= 4:
            df_bat = df_bat.iloc[:, :5] # Limit to 5 cols if extra present
            df_bat.columns = ["Rank", "Player", "Country", "Rating", "ID"][:len(df_bat.columns)]

        col_table, col_chart = st.columns([1, 1])

        with col_table:
            st.markdown(f"**{selected_fmt} Batting Rankings — Top {len(df_bat)}**")
            for _, row in df_bat.iterrows():
                rank_val = row.get("Rank", 0)
                medal = "🥇" if rank_val == "1" or rank_val == 1 else ("🥈" if rank_val == "2" or rank_val == 2
                        else ("🥉" if rank_val == "3" or rank_val == 3 else f"#{rank_val}"))
                st.markdown(f"""
                <div style="display:flex;align-items:center;padding:6px 10px;
                            border-bottom:1px solid #1f2937;gap:12px">
                    <span style="width:40px;font-weight:700;color:#58a6ff">{medal}</span>
                    <span style="flex:1;color:#e2e8f0;font-weight:600">{row['Player']}</span>
                    <span style="color:#8b949e;font-size:0.85rem;width:100px">{row['Country']}</span>
                    <span style="color:#3fb950;font-weight:700;width:60px">{row['Rating']}</span>
                </div>
                """, unsafe_allow_html=True)

        with col_chart:
            st.markdown(f"**Rating Comparison**")
            fig = px.bar(
                df_bat.head(10),
                x="Rating", y="Player",
                orientation="h",
                color="Rating",
                color_continuous_scale="Blues",
                title=f"Top 10 {selected_fmt} Batsmen by Rating",
            )
            fig.update_layout(**_PLOTLY_LAYOUT)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No batting data available.")

    # DB batting stats
    st.markdown("---")
    st.markdown(f'<div class="section-title">📋 Database — {selected_fmt} Batting Stats</div>',
                unsafe_allow_html=True)

    db_bat = utils.run_query(f"""
        SELECT p.full_name AS Player, t.team_name AS Team,
               bs.matches AS Matches, bs.innings AS Innings,
               bs.runs_scored AS Runs, bs.highest_score AS 'High Score',
               ROUND(bs.batting_avg,2) AS Average,
               ROUND(bs.strike_rate,1) AS 'Strike Rate',
               bs.centuries AS '100s', bs.half_centuries AS '50s'
        FROM   batting_stats bs
        JOIN   players p ON bs.player_id = p.player_id
        JOIN   teams  t ON p.team_id    = t.team_id
        WHERE  bs.format = '{selected_fmt}'
        ORDER  BY bs.runs_scored DESC
        LIMIT  20
    """)
    if db_bat:
        df_db_bat = pd.DataFrame(db_bat)
        st.dataframe(df_db_bat, use_container_width=True, hide_index=True)

        fig2 = px.scatter(
            df_db_bat,
            x="Runs", y="Average",
            size="100s" if "100s" in df_db_bat.columns else None,
            color="Team",
            hover_name="Player",
            title=f"{selected_fmt} Runs vs Batting Average",
            size_max=20,
        )
        fig2.update_layout(**_PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

# TAB 2 — TOP BOWLERS (API rankings)
with tab_bowl:
    st.markdown('<div class="section-title">🎯 Top Bowling Rankings (Cricbuzz API)</div>',
                unsafe_allow_html=True)

    with st.spinner(f"Loading {selected_fmt} bowling rankings..."):
        bowl_data = utils.get_top_bowling_stats(selected_fmt)

    if bowl_data:
        df_bowl = pd.DataFrame(bowl_data)
        if len(df_bowl.columns) >= 4:
            df_bowl = df_bowl.iloc[:, :5]
            df_bowl.columns = ["Rank", "Player", "Country", "Rating", "ID"][:len(df_bowl.columns)]

        col_t, col_c = st.columns([1, 1])
        with col_t:
            st.markdown(f"**{selected_fmt} Bowling Rankings**")
            for _, row in df_bowl.iterrows():
                rank_val = row.get("Rank", 0)
                medal = "🥇" if rank_val == "1" or rank_val == 1 else ("🥈" if rank_val == "2" or rank_val == 2
                        else ("🥉" if rank_val == "3" or rank_val == 3 else f"#{rank_val}"))
                st.markdown(f"""
                <div style="display:flex;align-items:center;padding:6px 10px;
                            border-bottom:1px solid #1f2937;gap:12px">
                    <span style="width:40px;font-weight:700;color:#f6ad55">{medal}</span>
                    <span style="flex:1;color:#e2e8f0;font-weight:600">{row['Player']}</span>
                    <span style="color:#8b949e;font-size:0.85rem;width:100px">{row['Country']}</span>
                    <span style="color:#fc8181;font-weight:700;width:60px">{row['Rating']}</span>
                </div>
                """, unsafe_allow_html=True)
        with col_c:
            fig = px.bar(
                df_bowl.head(10), x="Rating", y="Player",
                orientation="h", color="Rating",
                color_continuous_scale="Reds",
                title=f"Top 10 {selected_fmt} Bowlers by Rating",
            )
            fig.update_layout(**_PLOTLY_LAYOUT)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    # DB bowling stats
    st.markdown("---")
    st.markdown(f'<div class="section-title">📋 Database — {selected_fmt} Bowling Stats</div>',
                unsafe_allow_html=True)

    db_bowl = utils.run_query(f"""
        SELECT p.full_name AS Player, t.team_name AS Team,
               bs.matches AS Matches,
               ROUND(bs.overs_bowled,1) AS Overs,
               bs.wickets_taken AS Wickets,
               bs.runs_conceded AS Runs,
               ROUND(bs.bowling_avg,2) AS Average,
               ROUND(bs.economy_rate,2) AS Economy,
               bs.best_bowling AS Best,
               bs.five_wickets AS '5W'
        FROM   bowling_stats bs
        JOIN   players p ON bs.player_id = p.player_id
        JOIN   teams  t ON p.team_id    = t.team_id
        WHERE  bs.format = '{selected_fmt}'
        ORDER  BY bs.wickets_taken DESC
        LIMIT  20
    """)
    if db_bowl:
        df_db_bowl = pd.DataFrame(db_bowl)
        st.dataframe(df_db_bowl, use_container_width=True, hide_index=True)

        fig3 = px.scatter(
            df_db_bowl,
            x="Economy", y="Wickets",
            size="Overs" if "Overs" in df_db_bowl.columns else None,
            color="Team",
            hover_name="Player",
            title=f"{selected_fmt} Economy Rate vs Wickets Taken",
            size_max=25,
        )
        fig3.update_layout(**_PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

# TAB 3 — DB CAREER STATS
with tab_db:
    st.markdown('<div class="section-title">📋 Career Statistics — Database</div>',
                unsafe_allow_html=True)

    players_list = utils.get_all_players()
    if players_list is not None and not (isinstance(players_list, list) and len(players_list) == 0):
        # Handle both DataFrame and List return types from bridge
        df_p_list = pd.DataFrame(players_list)
        player_names = df_p_list["full_name"].tolist()
        selected_player = st.selectbox("Select a player", player_names, key="player_select")
        player_row = df_p_list[df_p_list["full_name"] == selected_player].iloc[0]

        if not player_row.empty:
            pid = player_row["player_id"]
            st.markdown(f"""
            <div class="stat-card" style="display:flex;gap:2rem;flex-wrap:wrap">
                <div>
                    <div style="font-size:1.4rem;font-weight:800;color:#e2e8f0">{player_row['full_name']}</div>
                    <div style="color:#8b949e">{player_row.get('playing_role','–')} | {player_row.get('team_name','–')}</div>
                </div>
                <div style="color:#6b7280;font-size:0.88rem">
                    <div>🏏 Bat: {player_row.get('batting_style','–')}</div>
                    <div>🎯 Bowl: {player_row.get('bowling_style','–')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_bat_c, col_bowl_c = st.columns(2)
            with col_bat_c:
                st.markdown("**Batting Career Stats**")
                bat_stats = utils.get_batting_stats(pid)
                if bat_stats is not None and len(bat_stats) > 0:
                    df_bc = pd.DataFrame(bat_stats)
                    st.dataframe(df_bc, use_container_width=True, hide_index=True)
                    fig_runs = px.bar(df_bc, x="format", y="runs_scored", color="format", title="Runs by Format")
                    fig_runs.update_layout(**_PLOTLY_LAYOUT, showlegend=False)
                    st.plotly_chart(fig_runs, use_container_width=True)

            with col_bowl_c:
                st.markdown("**Bowling Career Stats**")
                bowl_stats = utils.get_bowling_stats(pid)
                if bowl_stats is not None and len(bowl_stats) > 0:
                    df_bwl = pd.DataFrame(bowl_stats)
                    st.dataframe(df_bwl, use_container_width=True, hide_index=True)
                    fig_wkt = px.bar(df_bwl, x="format", y="wickets_taken", color="format", title="Wickets by Format")
                    fig_wkt.update_layout(**_PLOTLY_LAYOUT, showlegend=False)
                    st.plotly_chart(fig_wkt, use_container_width=True)
    else:
        st.info("No players found in database.")

# TAB 4 — PLAYER SEARCH
with tab_search:
    st.markdown('<div class="section-title">🔍 Player Search</div>', unsafe_allow_html=True)
    search_term = st.text_input("Search player by name", placeholder="e.g. Kohli, Bumrah...")
    if search_term:
        from utils.db_connection import search_players
        results = search_players(search_term)
        if results is not None and len(results) > 0:
            st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        else:
            st.warning("No players found.")

# Footer 
st.markdown("<br><div style='text-align:center;color:#484f58;font-size:0.8rem;border-top:1px solid #21262d;padding-top:1rem'>📊 Rankings from Cricbuzz API · Career stats from local SQLite database</div>", unsafe_allow_html=True)