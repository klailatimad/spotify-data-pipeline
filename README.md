
# Spotify Simulation Data Pipeline (Local)

This project simulates a Spotify-like batch data pipeline using real track metadata and synthetic user activity. It's built fully locally using Python, PostgreSQL (via Docker), dbt for modeling, and Streamlit for interactive dashboards.

---

## 🧱 Project Structure

```plaintext
spotify_de_project/
├── data/
│   ├── spotify_tracks.csv
│   ├── users.csv
│   └── user_activity_<YYYY-MM-DD>.csv
├── dashboard.py
├── docker-compose.yml
├── .env
├── collect_songs.py
├── generate_users.py
├── generate_user_activity.py
├── load_csvs_to_postgres.py
├── spotify_dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── raw/
│   │   ├── staging/
│   │   └── dw/
└── README.md
```

---

## ✅ Steps to Run Locally

### 1. Install Dependencies
Run:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install spotipy pandas faker psycopg2-binary python-dotenv streamlit sqlalchemy
```

### 2. Set Up PostgreSQL (via Docker)
Run:
```bash
docker compose up -d
```

### 3. Collect Metadata & Generate Synthetic Data
- **Spotify tracks (one-time):**
    ```bash
    python collect_songs.py
    ```
- **Users (one-time):**
    ```bash
    python generate_users.py
    ```
- **Daily listening events (can be run repeatedly):**
    ```bash
    python generate_user_activity.py
    ```

### 4. Load Data into Postgres
Includes ETL logging to avoid reprocessing already loaded files:
```bash
python load_csvs_to_postgres.py
```

---

## 🧱 Data Stack

- **Storage:** PostgreSQL (via Docker)
- **Ingestion:** Python scripts + Pandas
- **Modeling:** dbt with layered approach (raw → staging → DW)
- **Dashboarding:** Streamlit
- **Orchestration (upcoming):** Airflow DAGs (planned)

---

## 📊 Dashboards

Run:
```bash
streamlit run dashboard.py
```

The dashboard includes:
- Total listens per day (line chart)
- Top genres and artists (bar charts)
- Skips vs completions
- Interactive filters by user, genre, artist

---

## 🛠 dbt Overview

Your dbt project (`spotify_dbt`) includes:
- **Source definitions:** Raw data from Postgres
- **Staging models:** Cleaned column naming & type casting
- **Fact & Dimension tables:**
    - `dim_users`, `dim_songs`
    - `fact_user_listening` (incremental by `event_id`)
- **Materializations:**
    - Views for staging
    - Tables for dimension
    - Incremental for fact

To run:
```bash
cd spotify_dbt
dbt build
```

---

## 🔮 Roadmap

- Add dbt models for transformations
- Implement Streamlit dashboard
- Add incremental load for fact table
- Skip already loaded CSVs via ETL log
- Orchestrate with Airflow DAG
- Move to cloud (e.g., Snowflake + S3)
- Add Dockerized API for pipeline triggers

---

## 💡 Project Goals

- End-to-end simulation of a modern data pipeline
- Practice ingestion, modeling, and analytics
- Build a project suitable for portfolio/GitHub
- Enable future transition to cloud-native architecture

---
