# Importing libraries
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime, timedelta
from scraper_func import scrap_data_A
from scrapbi_multi_page import scrape_search_results
from airflow.hooks.mysql_hook import MySqlHook

import pandas as pd

# Default settings for all the dags in the pipeline
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 1),
    'depends_on_past': False,
    'max_active_runs_per_dag': 1,
    'retries': 0,
    'retries_delay': timedelta(minutes=5)
}

# Load to MySQL function
def load_to_mysql_A(**kwargs):
    ti = kwargs['ti']

    # Retrieve data_frame_A from XCom
    data_frame_A = ti.xcom_pull(task_ids='scraping_data_A', key='data_frame')

    # Check if data_frame_A is None
    if data_frame_A is None:
        print("No data found. Skipping load_to_mysql_A task.")
        return

    # Create CSV file with the current date in the file name
    current_date = date.today().strftime("%Y-%m-%d")
    csv_file_path_A = f'/data/data_bahan_pokok_scrap_{current_date}.csv'

    # Save DataFrame to CSV file
    data_frame_A.to_csv(csv_file_path_A, index=False, header=False, sep=";")

    # Use Airflow MySQLHook to execute LOAD DATA INFILE
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()

    # Table Name for Program Scraping A
    table_name_A = "scrape_harga"

    try:
        # Use MySQLHook's execute method to load data using LOAD DATA INFILE
        query_A = f"LOAD DATA INFILE '{csv_file_path_A}' REPLACE INTO TABLE {table_name_A} FIELDS TERMINATED BY ';' IGNORE 1 LINES;"
        cursor.execute(query_A)

        connection.commit()
        print(f"Data loaded into {table_name_A}")
    except Exception as e:
        connection.rollback()
        print(f"Error loading data: {e}")
    finally:
        cursor.close()
        connection.close()

# Load to MySQL function for Table B
def load_to_mysql_B(**kwargs):
    ti = kwargs['ti']

    # Retrieve data_frame_B from XCom
    data_frame_B = ti.xcom_pull(task_ids='scraping_data_B', key='scraped_data')

    # Check if data_frame_B is None
    if data_frame_B is None:
        print("No search results found. Skipping load_to_mysql_B task.")
        return

    # Create CSV file with the current date in the file name
    current_date = date.today().strftime("%Y-%m-%d")
    csv_file_path_B = f'/data/bisnis_search_results_multi_page_{current_date}.csv'

    # Save DataFrame to CSV file
    data_frame_B.to_csv(csv_file_path_B, index=False, header=False, sep=";")

    # Use Airflow MySQLHook to execute LOAD DATA INFILE
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')  # Replace with your MySQL connection ID
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()

    # Table Name for Program Scraping B
    table_name_B = "scrape_berita"

    try:
        # Use MySQLHook's execute method to load data using LOAD DATA INFILE
        query_B = f"LOAD DATA INFILE '{csv_file_path_B}' REPLACE INTO TABLE {table_name_B} FIELDS TERMINATED BY ';' IGNORE 1 LINES;"
        cursor.execute(query_B)

        connection.commit()
        print(f"Data loaded into {table_name_B}")
    except Exception as e:
        connection.rollback()
        print(f"Error loading data: {e}")
    finally:
        cursor.close()
        connection.close()

# Define the DAG
dag = DAG(
    dag_id='Scrape_Pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

# DAG 1 [Dummy Start Task]
start_task = DummyOperator(
    task_id="start_task",
    dag=dag,
)

# DAG 2 [Scrap Data A]
scrap_data_task_A = PythonOperator(
    task_id="scraping_data_A",
    python_callable=scrap_data_A,
    provide_context=True,
    dag=dag,
)

# DAG 3 [Load Data A to MySQL]
load_to_mysql_task_A = PythonOperator(
    task_id="load_to_mysql_A",
    python_callable=load_to_mysql_A,
    provide_context=True,
    dag=dag,
)

# DAG 4 [Scrap Data B]
def run_scrap_task_B(**kwargs):
    keyword = "UMKM"
    max_pages = 1
    all_results_df = scrape_search_results(keyword, max_pages, **kwargs)

    if not all_results_df.empty:
        output_file = f'/data/bisnis_search_results_multi_page_{date.today()}.csv'
        all_results_df.to_csv(output_file, index=False, header=False, sep=";")
        print(f"Scraped {len(all_results_df)} search results and saved to {output_file}")
    else:
        print("No search results found.")

scrap_data_task_B = PythonOperator(
    task_id="scraping_data_B",
    python_callable=run_scrap_task_B,
    provide_context=True,
    dag=dag,
)

# DAG 5 [Load Data B to MySQL]
load_to_mysql_task_B = PythonOperator(
    task_id="load_to_mysql_B",
    python_callable=load_to_mysql_B,
    provide_context=True,
    dag=dag,
)

# DAG 6 [Dummy Finish Task]
finish_task = DummyOperator(
    task_id="finish_task",
    dag=dag,
)

# Set task dependencies
start_task >> scrap_data_task_A >> load_to_mysql_task_A >> scrap_data_task_B >> load_to_mysql_task_B >> finish_task
