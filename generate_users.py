# generate_users.py

import os
import random
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)

# -------- SETTINGS --------
NUM_USERS = 1000
OUTPUT_FILE = "data/users.csv"
GENRES = ['pop', 'rock', 'hip-hop', 'edm', 'jazz', 'indie', 'classical', 'metal', 'reggae', 'country']
COUNTRIES = ['US', 'CA', 'GB', 'DE', 'FR', 'IN', 'BR', 'AU', 'JP']

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Generate users
users = []
for i in range(NUM_USERS):
    user_id = f"U{i:04}"
    users.append({
        'user_id': user_id,
        'age': random.randint(16, 60),
        'country': random.choice(COUNTRIES),
        'preferred_genre': random.choice(GENRES),
        'signup_date': fake.date_between(start_date='-2y', end_date='today')
    })

users_df = pd.DataFrame(users)
users_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Generated and saved {NUM_USERS} users to {OUTPUT_FILE}")
