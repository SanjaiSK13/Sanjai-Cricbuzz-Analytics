import streamlit as st
import pandas as pd
from utils.db_connection import execute_crud, run_query

st.title("🛠️ Player Management System")

def get_all_player_names():
    df = run_query("SELECT player_name FROM player_stats ORDER BY player_name ASC")
    if not df.empty:
        return df['player_name'].tolist()
    return []

# 3. The 4 Main Operations
tab1, tab2, tab3, tab4 = st.tabs(["🟢 CREATE", "🔵 READ", "🟠 UPDATE", "🔴 DELETE"])

# Create Operation
with tab1:
    st.subheader("Add New Player Record")
    st.caption("Manually assign a unique Player ID.")
    
    with st.form("create_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            new_id = st.number_input("Player ID (Unique)", min_value=1, step=1, value=18)
            new_name = st.text_input("Player Name", value="Virat Kohli")
            new_matches = st.number_input("Matches Played", min_value=0, step=1, value=295)
            
        with col_b:
            new_runs = st.number_input("Total Runs", min_value=0, step=1, value=13906)
            new_avg = st.number_input("Batting Average", min_value=0.0, step=0.01, format="%.2f", value=58.18)
        
        submitted = st.form_submit_button("Add Player to Database")
        
        if submitted:
            if new_name and new_id:
                # 1. Check if ID exists
                id_check = run_query("SELECT * FROM player_stats WHERE player_id = :id", {"id": new_id})
                # 2. Check if Name exists
                name_check = run_query("SELECT * FROM player_stats WHERE player_name = :name", {"name": new_name})
                
                if not id_check.empty:
                    st.error(f"⚠️ Error: Player ID {new_id} is already taken!")
                elif not name_check.empty:
                    st.error(f"⚠️ Error: Player '{new_name}' already exists!")
                else:
                    sql = """
                        INSERT INTO player_stats (player_id, player_name, matches, runs, average)
                        VALUES (:id, :name, :matches, :runs, :avg)
                    """
                    params = {
                        "id": new_id, "name": new_name, 
                        "matches": new_matches, "runs": new_runs, "avg": new_avg
                    }
                    res = execute_crud(sql, params)
                    if res == "Success":
                        st.success(f"✅ Successfully added {new_name}!")
                        st.cache_data.clear() # Clear cache so name appears in dropdowns immediately
                    else:
                        st.error(res)
            else:
                st.warning("Player ID and Name are required.")

# Read Operation
with tab2:
    st.subheader("Current Database Records")
    if st.button("🔄 Refresh Data"):
        st.rerun()
        
    sql = "SELECT player_id, player_name, matches, runs, average FROM player_stats ORDER BY player_id ASC"
    df = run_query(sql)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Database is empty.")

# Update Function
with tab3:
    st.subheader("Update Player Details")
    
    # Get latest list of players for the dropdown
    player_list = get_all_player_names()
    
    # The Dropdown (Acts as Search-as-you-type)
    selected_player_upd = st.selectbox(
        "🔍 Select Player to Update", 
        options=[""] + player_list,  # Add empty option at start
        index=0
    )
    
    if selected_player_upd:
        # Fetch current details
        search_query = "SELECT * FROM player_stats WHERE player_name = :name"
        search_res = run_query(search_query, {"name": selected_player_upd})
        
        if not search_res.empty:
            current_data = search_res.iloc[0]
            
            with st.form("update_form"):
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Player ID (Read-Only)", value=str(current_data['player_id']), disabled=True)
                    up_matches = st.number_input("Matches", value=int(current_data['matches']))
                    up_runs = st.number_input("Runs", value=int(current_data['runs']))
                with c2:
                    st.text_input("Name (Read-Only)", value=str(current_data['player_name']), disabled=True)
                    up_avg = st.number_input("Average", value=float(current_data['average']))
                
                p_id = int(current_data['player_id'])
                update_btn = st.form_submit_button("💾 Save Changes")
                
                if update_btn:
                    sql = """
                        UPDATE player_stats 
                        SET matches=:matches, runs=:runs, average=:avg 
                        WHERE player_id=:pid
                    """
                    params = {
                        "matches": up_matches, "runs": up_runs, 
                        "avg": up_avg, "pid": p_id
                    }
                    res = execute_crud(sql, params)
                    if res == "Success":
                        st.success(f"✅ Updated details for {selected_player_upd}")
                    else:
                        st.error(res)

# Delete Function
with tab4:
    st.subheader("Delete Player Record")
    
    # Get latest list of players
    player_list_del = get_all_player_names()
    
    # Searchable Dropdown
    selected_player_del = st.selectbox(
        "🗑️ Select Player to Delete", 
        options=[""] + player_list_del, 
        index=0
    )
    
    if selected_player_del:
        st.warning(f"You are about to delete: **{selected_player_del}**")
        confirm_check = st.checkbox("I confirm that I want to delete this player permanently")
        
        if st.button("🗑️ Delete Player", type="primary"):
            if confirm_check:
                sql = "DELETE FROM player_stats WHERE player_name = :name"
                res = execute_crud(sql, {"name": selected_player_del})
                if res == "Success":
                    st.success(f"✅ Player '{selected_player_del}' deleted.")
                    # We usually rerun to refresh the dropdown list
                    st.rerun()
                else:
                    st.error(res)
            else:
                st.error("Please check the confirmation box.")
