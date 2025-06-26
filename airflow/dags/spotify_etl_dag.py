from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments
default_args = {
    'owner': 'imad',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id='spotify_etl_pipeline',
    default_args=default_args,
    description='Run Spotify ETL pipeline scripts in order',
    schedule_interval='@daily',  # or '@once' for manual
    start_date=datetime(2025, 6, 25),
    catchup=False,
) as dag:

    # collect_songs = BashOperator(
    #     task_id='collect_songs',
    #     bash_command='python /opt/airflow/dags/scripts/collect_songs.py',
    # )

    # generate_users = BashOperator(
    #     task_id='generate_users',
    #     bash_command='python /opt/airflow/dags/scripts/generate_users.py',
    # )

    generate_user_activity = BashOperator(
        task_id='generate_user_activity',
        bash_command='python /opt/airflow/dags/scripts/generate_user_activity.py',
    )

    load_csvs_to_postgres = BashOperator(
        task_id='load_csvs_to_postgres',
        bash_command='python /opt/airflow/dags/scripts/load_csvs_to_postgres.py',
    )

    # Task sequence
    # collect_songs >> generate_users >> 
    generate_user_activity >> load_csvs_to_postgres
