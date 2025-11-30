import streamlit as st
import pandas as pd
from utils.db_connection import run_query
from utils.api_handler import fetch_match_scorecard

st.set_page_config(page_title="Cricket Dashboard", page_icon="🏏", layout="wide")

# Main UI
st.title("📡 Cricbuzz Live Match Dashboard")
matches_query = """
    SELECT match_id, series_name, team1, team2, winner, match_desc 
    FROM matches 
    WHERE data_source = 'real' 
    ORDER BY match_date DESC
"""
matches_df = run_query(matches_query)

if matches_df.empty:
    st.warning("No live matches found in database. Please run `python real_data_loader.py` to fetch data.")
else:
    match_options = {
        f"{row['team1']} vs {row['team2']} - {row['match_desc']}": row['match_id'] 
        for index, row in matches_df.iterrows()
    }
    
    selected_label = st.selectbox("🎯 Select a Match", list(match_options.keys()))
    
    if selected_label:
        selected_id = match_options[selected_label]
        match_info = matches_df[matches_df['match_id'] == selected_id].iloc[0]
        st.divider()
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {match_info['team1']} vs {match_info['team2']}")
            st.caption(f"Series: {match_info['series_name']}")
            status_text = f"{match_info['winner']}" if match_info['winner'] else "Match in Progress"
            st.info(f"📌 **Status:** {status_text}")
            
        with col2:
            if st.button("🔴 Load Full Scorecard", type="primary"):
                st.rerun()

        st.subheader("📋 Detailed Scorecard")
        with st.spinner("Fetching latest scorecard..."):
            scorecard_data = fetch_match_scorecard(selected_id)
            
            if scorecard_data and 'scoreCard' in scorecard_data:
               
                for innings in scorecard_data['scoreCard']:
                    inn_name = innings.get('batTeamDetails', {}).get('batTeamShortName', 'Innings')
                    st.markdown(f"#### 🏏 {inn_name} Batting")

                    if 'batTeamDetails' in innings and 'batsmenData' in innings['batTeamDetails']:
                        batsmen_list = []
                        for bat in innings['batTeamDetails']['batsmenData'].values():
                            batsmen_list.append({
                                "Batsman": bat.get('batName'),
                                "Runs": bat.get('runs'),
                                "Balls": bat.get('balls'),
                                "4s": bat.get('fours'),
                                "6s": bat.get('sixes'),
                                "SR": bat.get('strikeRate')
                            })
                        
                        if batsmen_list:
                            df_bat = pd.DataFrame(batsmen_list)
                            st.dataframe(
                                df_bat, 
                                use_container_width=True, 
                                hide_index=True,
                                column_config={
                                    "Runs": st.column_config.NumberColumn(format="%d"),
                                    "Balls": st.column_config.NumberColumn(format="%d")
                                }
                            )
                    else:
                        st.write("No batting data available yet.")
                    
                    st.divider()
            else:
                st.warning("Scorecard not available for this match yet.")
