# generate_user_activity.py

import os
import random
import pandas as pd
from datetime import datetime, timedelta

# -------- SETTINGS --------
# SONGS_FILE = "data/spotify_tracks.csv" # Path for local testing
SONGS_FILE = "/opt/airflow/data/spotify_tracks.csv" 
# USERS_FILE = "data/users.csv" # Path for local testing
USERS_FILE = "/opt/airflow/data/users.csv" # Path for Airflow
TODAY = datetime.today().date()
# OUTPUT_FILE = f"data/user_activity_{TODAY}.csv" # Path for local testing
OUTPUT_FILE = f"/opt/airflow/data/user_activity_{TODAY}.csv" # Path for Airflow

DEVICE_TYPES = ['mobile', 'desktop', 'web', 'tablet']

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# -------- LOAD SONG DATA --------
songs_df = pd.read_csv(SONGS_FILE)
assert not songs_df.empty, "spotify_tracks.csv is missing or empty."

# -------- LOAD USER DATA --------
assert os.path.exists(USERS_FILE), "users.csv not found. Run generate_users.py first."
users_df = pd.read_csv(USERS_FILE)

# -------- SIMULATE ACTIVITY --------
activity = []
event_counter = 0

for _, user in users_df.iterrows():
    plays_today = random.randint(5, 20)
    genre_songs = songs_df[songs_df['genre'] == user['preferred_genre']]
    if genre_songs.empty:
        genre_songs = songs_df

    for _ in range(plays_today):
        song = genre_songs.sample(1).iloc[0]
        completed = random.choices([True, False], weights=[0.8, 0.2])[0]
        duration = song['duration_ms']
        listened = duration if completed else int(duration * random.uniform(0.1, 0.6))

        # Random timestamp for today between 6 AM and 11:59 PM
        rand_hour = random.randint(6, 23)
        rand_min = random.randint(0, 59)
        rand_sec = random.randint(0, 59)
        timestamp = datetime.combine(TODAY, datetime.min.time()) + timedelta(
            hours=rand_hour, minutes=rand_min, seconds=rand_sec)

        activity.append({
            'event_id': f"{TODAY.strftime('%Y%m%d')}_E{event_counter:07}",
            'user_id': user['user_id'],
            'track_id': song['track_id'],
            'timestamp': timestamp,
            'duration_ms': listened,
            'completed': completed,
            'skipped': not completed,
            'device_type': random.choice(DEVICE_TYPES),
            'location': user['country']
        })
        event_counter += 1

activity_df = pd.DataFrame(activity)
activity_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Simulated {len(activity)} user activity events and saved to {OUTPUT_FILE}")
