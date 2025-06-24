from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection
DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

st.title("Spotify User Listening Dashboard")

# --- Total listens by day ---
listens_per_day = pd.read_sql("""
    SELECT DATE(timestamp) as date, COUNT(*) as total_listens
    FROM staging_dw.fact_user_listening
    GROUP BY DATE(timestamp)
    ORDER BY date;
""", engine)
st.subheader("Total Listens Per Day")
st.line_chart(listens_per_day.set_index("date"))

# --- Top genres ---
top_genres = pd.read_sql("""
    SELECT s.genre, COUNT(*) as plays
    FROM staging_dw.fact_user_listening f
    JOIN staging_dw.dim_songs s ON f.track_id = s.track_id
    GROUP BY s.genre
    ORDER BY plays DESC
    LIMIT 10;
""", engine)
st.subheader("Top Genres")
st.bar_chart(top_genres.set_index("genre"))

# --- Skips vs Completions ---
skip_completion = pd.read_sql("""
    SELECT
      SUM(CASE WHEN skipped THEN 1 ELSE 0 END) AS skipped,
      SUM(CASE WHEN completed THEN 1 ELSE 0 END) AS completed
    FROM staging_dw.fact_user_listening;
""", engine)
st.subheader("Skips vs Completions")
st.bar_chart(skip_completion.T)

# --- Top Artists Overall ---
top_artists = pd.read_sql("""
    SELECT s.artist_name, COUNT(*) AS plays
    FROM staging_dw.fact_user_listening f
    JOIN staging_dw.dim_songs s ON f.track_id = s.track_id
    GROUP BY s.artist_name
    ORDER BY plays DESC
    LIMIT 10;
""", engine)
st.subheader("Top Artists Overall")
st.bar_chart(top_artists.set_index("artist_name"))

# --- Top Artists Per User ---
users = pd.read_sql("SELECT DISTINCT user_id FROM staging_dw.fact_user_listening", engine)
selected_user = st.selectbox("Select a user to view their top artists:", users['user_id'])

user_top_artists = pd.read_sql(f"""
    SELECT s.artist_name, COUNT(*) AS plays
    FROM staging_dw.fact_user_listening f
    JOIN staging_dw.dim_songs s ON f.track_id = s.track_id
    WHERE f.user_id = '{selected_user}'
    GROUP BY s.artist_name
    ORDER BY plays DESC
    LIMIT 5;
""", engine)
st.subheader(f"Top 5 Artists for User {selected_user}")
st.bar_chart(user_top_artists.set_index("artist_name"))
