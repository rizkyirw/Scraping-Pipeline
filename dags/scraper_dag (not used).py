from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator  # Import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime, timedelta
from scraper_func import scrap_data_A # Importing scrap_data function from scraper_func.py
from scrapbi_multi_page import scrape_search_results # Importing scraping news from scrapbi_multi_page.py

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

with DAG(
    dag_id='Scrape_Pipeline_Not_Used',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=True
) as dag:
    
    # DAG 1 [Dummy Start Task]
    start_task = DummyOperator(
        task_id="start_task",
        dag=dag,
    )
    
    # DAG 2 [Scrap Data A]
    scrap_data_task_A = PythonOperator(
        task_id="scraping_data_A",
        python_callable=scrap_data_A, # Call the scrap data A function
        dag=dag,
    )

    # DAG 3 [Scrap Data B]
    def run_scrap_task_B():
        keyword = "UMKM"
        max_pages = 1
        all_results = scrape_search_results(keyword, max_pages)

        if all_results:
            df = pd.DataFrame(all_results)
            output_file = f"./dags/bisnis_search_results_multi_page_{date.today()}.csv"
            df.to_csv(output_file, index=False, sep=";")
            print(f"Scraped {len(all_results)} search results and saved to {output_file}")
        else:
            print("No search results found.")

    scrap_data_task_B = PythonOperator(
        task_id="scraping_data_B",
        python_callable=run_scrap_task_B, # Call the scrap data B function
        dag=dag,
    )

    # DAG 4 [Dummy Finish Task]
    finish_task = DummyOperator(
        task_id="finish_task",
        dag=dag,
    )

# Set task dependencies
start_task >> scrap_data_task_A >> scrap_data_task_B >> finish_task