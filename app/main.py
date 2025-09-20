import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import app.database as db   # <-- MySQL connector inside
import app.processing as processing
import app.deepseek_ai as deepseek
import app.visualization as visualization
import app.csv_ai as csv_ai
import re

# Configure Streamlit page
st.set_page_config(page_title="AI Financial Budgeting", layout="wide")

# Title & Description
st.title("💰 Deepseek MoneyMind")
st.write("Upload your transaction CSV file OR ask AI financial questions based on past data.")

# Create Tabs for Two Separate Workflows
tab1, tab2 = st.tabs(["📂 Upload CSV", "🤖 Ask AI"])

# -------------------- Tab 1: CSV Upload --------------------
with tab1:
    name = st.selectbox("Select Name", options=["Name 1", "Name 2"], index=0)
    uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"])

    if uploaded_file:
        df = processing.clean_and_process_csv(uploaded_file)
        df["Name"] = name  

        st.subheader("📊 Uploaded Transactions")
        st.dataframe(df)  

        st.subheader("📊 Spending Overview")
        visualization.plot_spending_chart(df)  

        if st.button("📥 Load Data into Database"):
            db.insert_transactions(df)
            st.success("Data successfully loaded into the MySQL database.")

        if st.button("🔍 Analyze with AI"):
            with st.spinner("🔄 Categorizing transactions with AI..."):
                categorized_df = csv_ai.batch_categorize_transactions(df)

            st.subheader("📊 AI-Categorized Transactions")
            st.dataframe(categorized_df)

            with st.spinner("💡 Generating insights with AI..."):
                insights = csv_ai.generate_insights(categorized_df)

            if insights:
                st.subheader("💡 AI-Generated Insights")
                st.markdown(insights)

# -------------------- Tab 2: AI Chat --------------------
with tab2:
    st.subheader("🤖 Deepseek Financial Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_sql" not in st.session_state:
        st.session_state.last_sql = ""
    if "last_sql_result" not in st.session_state:
        st.session_state.last_sql_result = ""
    if "thinking" not in st.session_state:
        st.session_state.thinking = False
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None

    # Chat history container
    chat_container = st.container()
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"🧑‍💼 **You:** {message}")
            else:
                st.markdown(f"🤖 **AI:** {message}")

    if st.session_state.last_sql:
        with st.expander("🔍 See Generated SQL Query"):
            st.code(st.session_state.last_sql, language="sql")

    if "last_think_text" in st.session_state and st.session_state.last_think_text:
        with st.expander("💭 AI's Thought Process"):
            if isinstance(st.session_state.last_think_text, list):
                for i, think_step in enumerate(st.session_state.last_think_text, start=1):
                    st.markdown(f"**Attempt {i}:**")
                    st.markdown(f" {think_step}\n")
            else:
                st.markdown(f"> {st.session_state.last_think_text}")

    if st.session_state.last_sql_result:
        with st.expander("📊 See SQL Execution Result"):
            st.write(st.session_state.last_sql_result)

# -------------------- Chat Input --------------------
# Must be OUTSIDE the tab to work correctly
user_query = st.chat_input("Ask AI about your finances...")

if user_query:
    st.session_state.pending_query = user_query
    st.session_state.thinking = True
    st.experimental_rerun()

if st.session_state.thinking and st.session_state.pending_query:
    with st.spinner("🤖 Thinking... Generating response..."):
        user_query = st.session_state.pending_query
        sql_query, ai_response, sql_result, think_text = deepseek.ask_financial_question(
            user_query, return_sql=True, return_result=True
        )

        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("🤖 AI", ai_response))

        st.session_state.last_sql = sql_query
        st.session_state.last_think_text = think_text
        st.session_state.last_sql_result = sql_result

        st.session_state.pending_query = None
        st.session_state.thinking = False
        st.experimental_rerun()
