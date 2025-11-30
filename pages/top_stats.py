import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_handler import fetch_icc_rankings, search_player, fetch_player_profile

st.set_page_config(page_title="Top Stats", page_icon="📈", layout="wide")
tab1, tab2 = st.tabs(["🏆 Global Rankings", "👤 Player Profile Search"])

with tab1:
    st.markdown("### 🌍 ICC Player Rankings")
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ["Batsmen", "Bowlers", "Allrounders"], index=0)
    with col2:
        match_format = st.selectbox("Format", ["Test", "ODI", "T20"], index=2)
    if st.button("Get Rankings"):
        with st.spinner(f"Fetching {match_format} {category}..."):
            df = fetch_icc_rankings(category.lower(), match_format.lower())          
            if not df.empty:
                cols_to_keep = [c for c in ['rank', 'name', 'country', 'rating'] if c in df.columns]
                clean_df = df[cols_to_keep].copy()
                st.dataframe(clean_df.head(10), use_container_width=True, hide_index=True)
                if 'country' in clean_df.columns:
                    st.subheader("Country Dominance (Top 50)")
                    fig = px.pie(clean_df.head(50), names='country', hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No ranking data found.")

with tab2:
    st.markdown("### 🔍 Search Player Profile")
    st.caption("Fetch detailed bio, stats, and personal info directly from Cricbuzz.")    
    search_query = st.text_input("Enter Player Name")  
    if st.button("Search Player", type="primary"):
        if search_query:
            with st.spinner("Searching..."):
                results = search_player(search_query)                
                if results:
                    player_options = {p['name']: p['id'] for p in results}                 
                    if player_options:
                        selected_name = st.selectbox("Select Player:", list(player_options.keys()))
                        
                        if selected_name:
                            p_id = player_options[selected_name]
                            profile = fetch_player_profile(p_id)
                            
                            if profile:
                                st.divider()
                                info = profile.get('personalInfo', {}) or profile.get('info', {}) or profile
                                img_id = profile.get('faceImageId', '')
                                head_col1, head_col2 = st.columns([1, 4])
                                
                                with head_col1:
                                    if img_id:
                                        img_url = f"https://images.cricbuzz.com/faces/170x170/{img_id}.jpg"
                                        st.image(img_url, width=150)
                                    else:
                                        st.image("https://via.placeholder.com/150?text=No+Image", width=150)
                                
                                with head_col2:
                                    st.subheader(profile.get('name', selected_name))                                    
                                    full_name = info.get('fullName') or info.get('name') or "N/A"
                                    born_date = info.get('born') or info.get('dateOfBirth') or "N/A"                                    
                                    st.markdown(f"**Full Name:** {full_name}")
                                    st.markdown(f"**Born:** {born_date}")

                                st.markdown("---")
                                col_a, col_b, col_c = st.columns(3)
                              
                                with col_a:
                                    st.markdown("#### 🏏 Cricket Details")
                                    st.write(f"**Role:** {info.get('role', 'N/A')}")
                                    st.write(f"**Batting:** {info.get('battingStyle', 'N/A')}")
                                    st.write(f"**Bowling:** {info.get('bowlingStyle', 'N/A')}")
                                    st.write(f"**Team:** {info.get('country', 'N/A')}")

                                with col_b:
                                    st.markdown("#### 📍 Personal Info")
                                    st.write(f"**Birth Place:** {info.get('birthPlace', 'N/A')}")
                                    st.write(f"**Height:** {info.get('height', 'N/A')}")
                                    
                                with col_c:
                                    st.markdown("#### 🏆 Teams")
                                    teams = profile.get('teams', [])
                                    if teams:
                                        if isinstance(teams, list) and len(teams) > 0:
                                            if isinstance(teams[0], dict):
                                                t_names = [t.get('teamName', '') for t in teams]
                                                st.info(", ".join(t_names))
                                            else:
                                                st.info(", ".join([str(t) for t in teams]))
                                    else:
                                        st.write("N/A")

                            else:
                                st.error("Profile found, but data was empty.")
                    else:
                        st.warning("Player ID not found.")
                else:
                    st.error("No players found. Try a different name.")
        else:
            st.warning("Please enter a player name to search.")
