import streamlit as st
import pandas as pd
from pathlib import Path
import utils # FIX: Use the synchronized bridge to avoid direct import errors

# Page config
st.set_page_config(
    page_title="CRUD Operations | Cricbuzz LiveStats",
    page_icon="🛠️",
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
def _success(msg: str) -> None:
    st.success(f"✅ {msg}")

def _error(msg: str) -> None:
    st.error(f"❌ {msg}")

def _teams_map() -> dict:
    # Use utils bridge for teams
    teams = utils.get_all_teams()
    if isinstance(teams, dict): return teams
    return {t["team_name"]: t["team_id"] for t in teams}

def _venues_map() -> dict:
    # Use utils bridge for venues
    venues = utils.get_all_venues()
    if isinstance(venues, dict): return venues
    return {f"{v['venue_name']}, {v['city']}": v["venue_id"] for v in venues}

# PAGE HEADER
st.markdown("""
<div style="background:linear-gradient(90deg,#1a1a2e,#0f3460);
            border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;
            border:1px solid #0f3460">
    <span style="font-size:1.8rem;font-weight:800;color:#e2e8f0">🛠️ CRUD Operations</span>
    <span style="color:#8b949e;margin-left:1rem">
        Create · Read · Update · Delete — full database management
    </span>
</div>
""", unsafe_allow_html=True)

# ENTITY TABS
tab_players, tab_matches, tab_venues, tab_stats, tab_audit = st.tabs([
    "👤 Players", "📅 Matches", "🏟️ Venues", "📊 Stats", "📋 Audit Log",
])

# TAB 1 — PLAYERS
with tab_players:
    st.markdown('<div class="section-title">👤 Player Management</div>',
                unsafe_allow_html=True)

    crud_mode = st.radio(
        "Operation", ["📋 View All", "➕ Add Player", "✏️ Edit Player", "🗑️ Delete Player"],
        horizontal=True, key="player_mode",
    )

    # VIEW
    if crud_mode == "📋 View All":
        search = st.text_input("🔍 Search by name, role, or country", key="p_search")
        players = utils.get_all_players()
        if search:
            q = search.lower()
            players = [p for p in players
                       if q in p.get("full_name","").lower()
                       or q in p.get("playing_role","").lower()
                       or q in p.get("nationality","").lower()]

        st.markdown(f"**{len(players)} player(s) found**")
        if players:
            df = pd.DataFrame(players)
            show_cols = ["player_id","full_name","team_name","playing_role",
                         "batting_style","bowling_style","nationality","date_of_birth"]
            df = df[[c for c in show_cols if c in df.columns]]
            df.columns = ["ID","Name","Team","Role","Bat Style","Bowl Style","Country","DOB"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Export CSV", csv, "players.csv", "text/csv", key="dl_players")

        # Role distribution
        if players:
            roles = {}
            for p in utils.get_all_players():
                role = p.get("playing_role") or "Unknown"
                roles[role] = roles.get(role, 0) + 1
            import plotly.express as px
            _LAY = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e2e8f0"), margin=dict(l=10,r=10,t=30,b=10))
            fig = px.pie(
                names=list(roles.keys()), values=list(roles.values()),
                title="Players by Role",
                color_discrete_sequence=["#58a6ff","#3fb950","#f6ad55","#fc8181"],
            )
            fig.update_layout(**_LAY)
            st.plotly_chart(fig, use_container_width=True)

    # ADD
    elif crud_mode == "➕ Add Player":
        st.markdown("**Add a new player to the database**")
        t_map = _teams_map()

        with st.form("add_player_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                full_name     = st.text_input("Full Name *")
                team_sel      = st.selectbox("Team *", list(t_map.keys()))
                role          = st.selectbox("Playing Role *", ["Batsman","Bowler","All-rounder","Wicket-keeper"])
                batting_style = st.selectbox("Batting Style", ["Right-hand bat","Left-hand bat"])
            with col2:
                bowling_style = st.text_input("Bowling Style", placeholder="e.g. Right-arm fast")
                nationality   = st.text_input("Nationality")
                dob           = st.text_input("Date of Birth (YYYY-MM-DD)", placeholder="1990-01-15")

            submitted = st.form_submit_button("➕ Add Player", type="primary", use_container_width=True)
            if submitted:
                if not full_name.strip():
                    _error("Full name is required.")
                else:
                    data = {
                        "full_name": full_name.strip(), "team_id": t_map[team_sel],
                        "playing_role": role, "batting_style": batting_style,
                        "bowling_style": bowling_style, "nationality": nationality, "date_of_birth": dob
                    }
                    # Map UI 'add_player' to DB 'insert_player'
                    res = utils.run_insert("""INSERT INTO players (full_name, team_id, playing_role, batting_style, bowling_style, nationality, date_of_birth) 
                                              VALUES (?,?,?,?,?,?,?)""", 
                                              (data["full_name"], data["team_id"], data["playing_role"], 
                                               data["batting_style"], data["bowling_style"], data["nationality"], data["date_of_birth"]))
                    if res > 0: _success(f"Player added with ID {res}.")
                    else: _error("Failed to add player.")

    # EDIT
    elif crud_mode == "✏️ Edit Player":
        st.markdown("**Edit an existing player**")
        players = utils.get_all_players()
        names_ids = {f"{p['full_name']} (ID {p['player_id']})": p["player_id"] for p in players}
        chosen = st.selectbox("Select player to edit", list(names_ids.keys()))
        pid = names_ids[chosen]
        row = utils.get_player_by_id(pid)
        t_map = _teams_map()

        if row:
            with st.form("edit_player_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Full Name", value=row["full_name"])
                    new_role = st.selectbox("Playing Role", ["Batsman","Bowler","All-rounder","Wicket-keeper"], 
                                            index=["Batsman","Bowler","All-rounder","Wicket-keeper"].index(row.get("playing_role","Batsman")))
                with col2:
                    new_nat  = st.text_input("Nationality", value=row.get("nationality","") or "")
                    new_dob  = st.text_input("Date of Birth", value=row.get("date_of_birth","") or "")

                if st.form_submit_button("💾 Save Changes", type="primary"):
                    # FIX: Handle integer response from utils.update_player
                    rc = utils.update_player(pid, new_name, row.get('team_id'), new_role, 
                                             row.get('batting_style'), row.get('bowling_style'), 
                                             new_nat, new_dob)
                    if (isinstance(rc, int) and rc > 0) or (isinstance(rc, dict) and rc.get("success")):
                        _success("Updated.")
                    else:
                        _error("Failed or no changes made.")

    # DELETE
    elif crud_mode == "🗑️ Delete Player":
        players = utils.get_all_players()
        names_ids = {f"{p['full_name']} (ID {p['player_id']})": p["player_id"] for p in players}
        chosen = st.selectbox("Select player to delete", list(names_ids.keys()))
        pid = names_ids[chosen]
        confirm = st.checkbox(f"Confirm delete player ID {pid}")
        if st.button("🗑️ Delete Player", type="primary", disabled=not confirm):
            # FIX: Handle integer response (rowcount) from utils.delete_player
            res = utils.delete_player(pid)
            if (isinstance(res, int) and res > 0) or (isinstance(res, dict) and res.get("success")):
                _success("Deleted."); st.rerun()
            else:
                _error("Delete failed.")

# TAB 2 — MATCHES
with tab_matches:
    match_mode = st.radio("Operation", ["📋 View All", "➕ Add Match", "🗑️ Delete Match"], horizontal=True)
    if match_mode == "📋 View All":
        matches = utils.get_all_matches()
        if matches is not None:
            # FIX: Scalar Index Fix
            data_m = [matches] if isinstance(matches, dict) else matches
            st.dataframe(pd.DataFrame(data_m), use_container_width=True, hide_index=True)
    elif match_mode == "🗑️ Delete Match":
        matches = utils.get_all_matches()
        m_ids = {f"{m['match_desc']}": m["match_id"] for m in (matches.to_dict('records') if hasattr(matches, 'to_dict') else matches)}
        chosen_m = st.selectbox("Select match", list(m_ids.keys()))
        if st.button("Delete"):
            # FIX: Handle result from delete_match
            res = utils.delete_match(m_ids[chosen_m])
            if (isinstance(res, int) and res > 0) or (isinstance(res, dict) and res.get("success")):
                 st.rerun()

# TAB 3 — VENUES
with tab_venues:
    st.markdown('<div class="section-title">🏟️ Venue Management</div>', unsafe_allow_html=True)
    v_list = utils.get_all_venues()
    if v_list:
        # FIX: Scalar Index Fix - wrap in list if it's a single dict
        data_v = [v_list] if isinstance(v_list, dict) else v_list
        st.dataframe(pd.DataFrame(data_v), use_container_width=True, hide_index=True)

# TAB 4 — STATS UPSERT
with tab_stats:
    st.markdown('<div class="section-title">📊 Batting & Bowling Stats</div>', unsafe_allow_html=True)
    stat_type = st.radio("Stat Type", ["🏏 Batting", "🎯 Bowling"], horizontal=True)
    players = utils.get_all_players()
    pmap = {f"{p['full_name']} (ID {p['player_id']})": p["player_id"] for p in players}
    chosen_p = st.selectbox("Select Player", list(pmap.keys()))
    pid = pmap[chosen_p]

    with st.form("stats_form"):
        fmt_sel = st.selectbox("Format", ["ODI","Test","T20I"])
        val = st.number_input("Runs/Wickets", min_value=0)
        if st.form_submit_button("Save"):
            if stat_type == "🏏 Batting":
                utils.upsert_batting_stats(pid, fmt_sel, 1, 1, val, val, val, 100.0, 0, 0)
            else:
                utils.upsert_bowling_stats(pid, fmt_sel, 1, val, val, 10.0, 20.0, 5.0, str(val)+"/0")
            _success("Saved.")

# TAB 5 — AUDIT LOG
with tab_audit:
    st.markdown('<div class="section-title">📋 Database Audit</div>', unsafe_allow_html=True)
    res = utils.run_query("SELECT * FROM players ORDER BY player_id DESC LIMIT 5")
    if res:
        # FIX: Scalar Index Fix
        data_res = [res] if isinstance(res, dict) else res
        st.table(data_res)

# Footer
st.markdown("<br><div style='text-align:center;color:#484f58;font-size:0.8rem;border-top:1px solid #21262d;padding-top:1rem'>🛠️ Database CRUD Management</div>", unsafe_allow_html=True)