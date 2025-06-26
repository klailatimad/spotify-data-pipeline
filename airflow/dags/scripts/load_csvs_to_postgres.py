import os
import psycopg2
import pandas as pd
from glob import glob
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv() # for local development
load_dotenv("/opt/airflow/.env") # for Airflow deployment


# ---------- SETTINGS ----------
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Local deployment
# DATA_DIR = "data"
# ACTIVITY_PATTERN = os.path.join(DATA_DIR, "user_activity_*.csv")
# TABLES = {
#     "users": os.path.join(DATA_DIR, "users.csv"),
#     "songs": os.path.join(DATA_DIR, "spotify_tracks.csv")
# }

# Airflow deployment
DATA_DIR = "/opt/airflow/data"
ACTIVITY_PATTERN = os.path.join(DATA_DIR, "user_activity_*.csv")
TABLES = {
    "users": os.path.join(DATA_DIR, "users.csv"),
    "songs": os.path.join(DATA_DIR, "spotify_tracks.csv")
}

# ---------- DB CONNECTION ----------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cur = conn.cursor()

# ---------- CREATE TABLES IF NOT EXISTS ----------
print("🔧 Creating tables if they don't exist...")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    age INT,
    country TEXT,
    preferred_genre TEXT,
    signup_date DATE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS songs (
    track_id TEXT PRIMARY KEY,
    track_name TEXT,
    artist_id TEXT,
    artist_name TEXT,
    duration_ms INT,
    genre TEXT,
    popularity INT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS user_activity (
    event_id TEXT PRIMARY KEY,
    user_id TEXT,
    track_id TEXT,
    timestamp TIMESTAMP,
    duration_ms INT,
    completed BOOLEAN,
    skipped BOOLEAN,
    device_type TEXT,
    location TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS etl_log (
    file_name TEXT PRIMARY KEY,
    loaded_at TIMESTAMP DEFAULT NOW()
);
""")

# ---------- UTILITY: Check if file already loaded ----------
def is_file_already_loaded(file_name):
    cur.execute("SELECT 1 FROM etl_log WHERE file_name = %s", (file_name,))
    return cur.fetchone() is not None

# ---------- LOAD USERS & SONGS ----------
def load_table_from_csv(table_name, csv_path):
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cur.fetchone()[0]
    if count > 0:
        print(f"⏩ Skipping {table_name}: already contains {count} rows.")
        return

    print(f"📥 Loading {table_name} from {csv_path}...")
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates(subset=[df.columns[0]])
    for _, row in df.iterrows():
        columns = ', '.join(row.index)
        values = ', '.join(['%s'] * len(row))
        sql = f"""
            INSERT INTO {table_name} ({columns}) VALUES ({values})
            ON CONFLICT ({row.index[0]}) DO NOTHING;
        """
        cur.execute(sql, tuple(row))
    print(f"✅ Loaded {len(df)} rows into {table_name}.")

for tbl, path in TABLES.items():
    load_table_from_csv(tbl, path)

# ---------- LOAD ALL NEW ACTIVITY FILES ----------
activity_files = sorted(glob(ACTIVITY_PATTERN))
total_events = 0

for file in activity_files:
    file_name = os.path.basename(file)

    if is_file_already_loaded(file_name):
        print(f"⏩ Skipping {file_name}: already loaded.")
        continue

    print(f"📥 Loading activity file: {file_name}")
    try:
        df = pd.read_csv(file)
        rows_loaded = 0

        for _, row in df.iterrows():
            values = tuple(row)
            sql = """
            INSERT INTO user_activity (
                event_id, user_id, track_id, timestamp, duration_ms,
                completed, skipped, device_type, location
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (event_id) DO NOTHING;
            """
            cur.execute(sql, values)
            rows_loaded += 1

        # Mark this file as loaded
        cur.execute("INSERT INTO etl_log (file_name) VALUES (%s)", (file_name,))
        total_events += rows_loaded
        print(f"✅ Loaded {rows_loaded} new events from {file_name} into user_activity.")

    except Exception as e:
        print(f"❌ Failed to load {file_name}: {e}")

print(f"🏁 Done. Total new events loaded: {total_events}")

# ---------- CLEANUP ----------
cur.close()
conn.close()
print("🏁 Done.")
