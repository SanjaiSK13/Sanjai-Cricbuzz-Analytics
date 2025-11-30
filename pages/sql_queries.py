import streamlit as st
from utils.queries import QUESTION_BANK
from utils.db_connection import run_query

st.set_page_config(page_title="SQL Analytics", page_icon="🧠", layout="wide")
st.title("🧠 SQL Query Lab")
st.markdown("Select a question from the list below to analyze your data.")
st.info("""
💡 **Pro Tip:** These queries run on the **Entire Database** (Mock History + Real Live Data). 
This allows you to analyze long-term trends (like 'Year-on-Year Performance') that wouldn't be possible with just 2 weeks of live API data.
""")

options = list(QUESTION_BANK.keys())

def format_func(option):
    return f"{option}: {QUESTION_BANK[option]['question']}"

selected_key = st.selectbox(
    "Select a Challenge:", 
    options, 
    format_func=format_func  # This makes it show "Question 1: Find players..."
)

q_data = QUESTION_BANK[selected_key]
st.divider()
col1, col2 = st.columns([1, 1])
with col1:
    show_sql = st.toggle("👁️ Show SQL Query")
with col2:
    run_btn = st.button("🚀 Run Query", type="primary")

if show_sql:
    st.markdown("##### SQL Command:")
    st.code(q_data['sql'], language='sql')

if run_btn:
    with st.spinner(f"Executing {selected_key}..."):
        result = run_query(q_data['sql'])
        if isinstance(result, str):
            st.error(f"SQL Error: {result}")
            if "no such table" in result.lower():
                st.warning("⚠️ This query relies on tables like `player_performance` or `partnerships`. You may need to add mock data in the CRUD page first.")
        elif result.empty:
            st.info("The query ran successfully, but returned 0 rows. (Try adding more data to the database!)")
        else:
            st.success(f"Query executed successfully! ({len(result)} rows found)")
            st.dataframe(result, use_container_width=True)
