import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

def main():
    st.title("🏏 Cricbuzz LiveStats Dashboard")
    
    st.markdown("""
    ### Welcome to the Cricket Analytics Platform
    This application integrates real-time cricket data with a powerful SQL database to provide analysis on players, matches, and historical trends.
    
    #### 👈 Use the Sidebar to Navigate:
    
    * **Live Matches:** View ongoing match scores and updates via API.
    * **Top Stats:** Visualizations of top run-scorers and wicket-takers.
    * **SQL Analytics:** Run the 25 predefined SQL questions to analyze the database.
    * **CRUD Operations:** Admin tools to Add, Update, or Delete player records.
    
    ---
    #### Project Stack
    * **Python & Streamlit:** For the frontend and logic.
    * **SQL (MySQL/Postgres):** For storing historical data and performing complex queries.
    * **Cricbuzz API:** For fetching real-time match data.
    """)

if __name__ == "__main__":
    main()
