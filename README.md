# Spotify Simulation Data Pipeline (Local)

This project simulates a Spotify-like batch data pipeline using real metadata and synthetic user activity — built entirely locally using Python, PostgreSQL (via Docker), and CSV ingestion.

---

## 🧱 Project Structure

```plaintext
spotify_de_project/
├── data/
│ ├── spotify_tracks.csv
│ ├── users.csv
│ └── user_activity_<YYYY-MM-DD>.csv
├── docker-compose.yml
├── generate_users.py
├── generate_user_activity.py
├── collect_songs.py
├── load_csvs_to_postgres.py
└── README.md
```
---

## ✅ Steps to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
Or install manually:

```
pip install spotipy pandas faker psycopg2-binary python-dotenv
```
### 2. Set Up PostgreSQL with Docker
```
docker compose up -d
```
### 3. Collect Spotify Songs (1st-time only)
```
python collect_songs.py
```
### 4. Generate Users (1st-time only)
```
python generate_users.py
```
### 5. Simulate Listening Activity (can be run daily)
```
python generate_user_activity.py
```
### 6. Load Data into Postgres
```
python load_csvs_to_postgres.py
```
---
## 🔮 Next Steps
 - Add dbt transformations: stg_, dim_, fact_
 - Create visual dashboards using Streamlit
 - Containerize the app for easier sharing
 - Abstract cloud-compatible pieces (e.g., S3 staging, Airflow DAGs)
 - Publish to GitHub with clean README, schema diagrams, and demo GIFs

---
## 💡 Project Goals
- Build a complete DE project for GitHub/portfolio
- Simulate user-centric streaming behavior
- Practice ingestion, warehousing, and analytics
- Optionally transition to a cloud-native pipeline (Snowflake + S3 + Airflow)
