import streamlit as st
import psycopg2
import requests

st.title("🤖 AI Learning Platform")

query = st.text_input("Ask me about a course...")

if st.button("Search"):
    if query:
        # Call ML service (or load TensorFlow model here directly)
        response = requests.get(
            "http://mlservice:8000/chatbot", params={"query": query}).json()

        # Connect to DB
        conn = psycopg2.connect(
            host="db", dbname="learning", user="postgres", password="postgres", port=5432
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM courses WHERE LOWER(category)=LOWER(%s) LIMIT 5", (response["category"],))
        courses = cur.fetchall()

        st.subheader("Bot Answer")
        st.write(response["response"])

        st.subheader("📚 Recommended Courses")
        for c in courses:
            st.write(f"- {c[1]} ({c[2]}): {c[3]}")
