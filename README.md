# Spotify Simulation Data Pipeline (Local)

This project simulates a Spotify-like batch data pipeline using real track metadata and synthetic user activity. It runs entirely locally using Python, PostgreSQL (via Docker), dbt for modeling, Airflow for orchestration, and Streamlit for interactive dashboards.

---

## 🧱 Project Structure

```plaintext
spotify_de_project/
├── airflow/
│   ├── dags/
│   │   ├── spotify_etl_dag.py
│   │   └── scripts/
│   │       ├── generate_user_activity.py
│   │       └── load_csvs_to_postgres.py
│   ├── logs/            # (ignored)
│   └── plugins/
├── data/                # Raw CSVs (ignored)
├── dashboard.py
├── docker-compose.yml
├── .env
├── collect_songs.py
├── generate_users.py
├── spotify_dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── raw/
│   │   ├── staging/
│   │   └── dw/
└── README.md
```
---
### ✅ Steps to Run Locally
1. Install Python Dependencies
`pip install -r requirements.txt`

	Or manually:

	`pip install spotipy pandas faker psycopg2-binary python-dotenv streamlit sqlalchemy`

2. Start the Docker Environment
This includes PostgreSQL and Airflow (scheduler & webserver):
`docker compose up -d`
> Wait ~1 minute for Airflow to finish initializing.

3. Access the Airflow UI
- Visit http://localhost:8080
   - Username: `airflow`
   - Password: `airflow`

- Enable and trigger the DAG: `spotify_etl_pipeline`.
It will:
  - Simulate and save new user activity
  - Load new data into PostgreSQL
  - Avoid reloading previously processed files using an etl_log table
---
### 📈 Running the Dashboard
Once the data is loaded:
`streamlit run dashboard.py`

The dashboard includes:

 - Total listens per day (line chart)
 - Top genres and artists (bar charts)
 - Skips vs completions   
 - Interactive filters (user, genre, artist)
---
### 🛠 Data Stack
|Layer|	Tool|
|-----|-----|
|Storage|	PostgreSQL (Docker)|
|Ingestion|	Python (Pandas, Spotipy)|
|Orchestration|	Apache Airflow|
|Modeling|	dbt (raw → staging → DW)|
|Analytics	|Streamlit|
---
### 💾 dbt Overview
Your dbt project (spotify_dbt) includes:
- Sources: Raw Postgres tables
- Staging Models: Column renaming, typing
- Warehouse Tables:
    - `dim_users`, `dim_songs`
    - `fact_user_listening` (incremental on `event_id`)

To run dbt:
```
cd spotify_dbt
dbt build
```
---
🔄 Airflow DAG
DAG: `spotify_etl_pipeline`
Tasks:
- `generate_user_activity`
   Simulates daily user behavior and writes to CSV
- `load_csvs_to_postgres`
Loads new CSVs into Postgres, skipping previously loaded files

The DAG is scheduled to run once per day.

---

### 🗺️ Roadmap
- [X] Setup local PostgreSQL + Airflow

 - [X] Automate user activity simulation via DAG

-  [X] Add ETL logging to prevent duplicates

 - [X] Build dashboard with filters

 - [x] Use dbt for transformations

 - [ ] Add dashboard update step to DAG

 - [ ] Abstract ingestion logic for reuse

 - [ ] Extend data with users, devices, genres, etc.

 - [ ] Optionally move pipeline to the cloud (e.g., S3 + Snowflake)

---
### 🎯 Project Goals
- Simulate a realistic batch analytics pipeline
- Practice orchestration, modeling, and dashboards
- Showcase a complete DE project in a local dev setup
- Build a foundation to evolve into a cloud-native stack