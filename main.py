import streamlit as st
from pathlib import Path
from utils.db_connection import init_db

#Page config (must be first Streamlit call)
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Bootstrap database on first run
@st.cache_resource
def _init():
    init_db()
    return True

_init()

#Sidebar navigation
with st.sidebar:
    st.markdown("## 🏏 Cricbuzz LiveStats")
    st.markdown("---")
    st.markdown("""
**Navigate using the pages above ↑**

| Page | Description |
|---|---|
| 🏠 Home | Overview & stats |
| 📺 Live | Live matches |
| 📊 Players | Top stats |
| 🔍 Analytics | 25 SQL queries |
| 🛠️ CRUD | Data management |
""")
    st.markdown("---")
    st.markdown("""
<small style='color:#666'>
Built with Python · Streamlit · SQLite · Cricbuzz API
</small>
""", unsafe_allow_html=True)

#Redirect to Home page
st.switch_page("pages/1_Home.py")