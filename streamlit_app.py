import streamlit as st
import psycopg2
import pandas as pd
import requests

# --- DB CONFIG ---
DB_CONFIG = {
    "dbname": "learning",
    "user": "postgres",
    "password": "postgres",
    "host": "db",       # when using docker-compose
    "port": "5432"
}

# For Streamlit Cloud, override with secrets if needed
# st.secrets["db_host"], st.secrets["db_user"], etc.

# --- Connect to DB ---


@st.cache_resource
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def run_query(query, params=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        if cur.description:  # SELECT
            return cur.fetchall(), [desc[0] for desc in cur.description]
        conn.commit()
    return [], []

# --- Pages ---


def chatbot_page():
    st.title("🤖 AI Learning Assistant")
    query = st.text_input("Ask me about a course...")

    if st.button("Search") and query.strip():
        try:
            # Call backend API (you can also directly call ML service)
            res = requests.get(
                "http://backend:5050/api/chatbot", params={"q": query})
            if res.status_code == 200:
                data = res.json()
                st.success(data.get("response", ""))
                st.subheader("📚 Recommended Courses")
                courses = data.get("courses", [])
                if courses:
                    for c in courses:
                        st.write(f"**{c['title']}** ({c['category']})")
                        st.caption(c["description"])
                else:
                    st.info("No courses found.")
            else:
                st.error("Backend error.")
        except Exception as e:
            st.error(f"Chatbot error: {e}")


def courses_page():
    st.title("📚 Available Courses")
    rows, cols = run_query("SELECT * FROM courses ORDER BY id ASC")
    if rows:
        df = pd.DataFrame(rows, columns=cols)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No courses available.")


def history_page():
    st.title("🕓 Search History")
    rows, cols = run_query(
        "SELECT * FROM search_logs ORDER BY id DESC LIMIT 20")
    if rows:
        df = pd.DataFrame(rows, columns=cols)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No history yet.")


def admin_page():
    st.title("📊 Admin Dashboard")
    try:
        res = requests.get("http://backend:5050/api/admin/stats")
        if res.status_code == 200:
            data = res.json()

            st.subheader("🔝 Categories by Search Count")
            st.write(pd.DataFrame(data["categories"]))

            st.subheader("⭐ Top Courses")
            st.write(pd.DataFrame(data["topCourses"]))
        else:
            st.error("Failed to fetch stats")
    except Exception as e:
        st.error(f"Stats error: {e}")


# --- Sidebar Navigation ---
PAGES = {
    "Chatbot": chatbot_page,
    "Courses": courses_page,
    "History": history_page,
    "Admin Dashboard": admin_page,
}

choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
PAGES[choice]()
