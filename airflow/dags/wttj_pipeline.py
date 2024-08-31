from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import os
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 22),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'simple_wttj_pipeline',
    default_args=default_args,
    description='Simple pipeline to process a single wttj JSON file',
    schedule_interval='30 8 * * *',  # Run daily at 8:30 AM UTC
    catchup=False,
)

JSON_SCRAPING_DIR = '/opt/airflow/ETL/Json_scraping'
JSON_TRANSFORMED_DIR = '/opt/airflow/ETL/Json_transformed'

def get_file_name(**kwargs):
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"wttj_database_{current_date}.json"
    file_path = os.path.join(JSON_SCRAPING_DIR, file_name)
    
    if os.path.exists(file_path):
        return file_path
    else:
        raise FileNotFoundError(f"File {file_name} does not exist in {JSON_SCRAPING_DIR}")

def clean_json(file_path, **kwargs):
    log_file = os.path.join('/opt/airflow/logs', f"{os.path.basename(file_path)}.log")

    subprocess.run(['python', '/opt/airflow/ETL/Transform/data_cleaning_wttj.py', file_path, JSON_TRANSFORMED_DIR, log_file], check=True)

    transformed_file_path = os.path.join(JSON_TRANSFORMED_DIR, f"{os.path.splitext(os.path.basename(file_path))[0]}_updated.json")
    return transformed_file_path

def bulk_load(**kwargs):
    ti = kwargs['ti']
    transformed_file_path = ti.xcom_pull(task_ids='clean_json_task')
    log_file = "/opt/airflow/logs/bulk_load_task.log"

    subprocess.run(['python', '/opt/airflow/ETL/Load/bulk_script_wttj.py', transformed_file_path, log_file], check=True)

with dag:
    start = DummyOperator(
        task_id='start'
    )

    get_file_name_task = PythonOperator(
        task_id='get_file_name',
        python_callable=get_file_name,
        provide_context=True,
    )

    clean_json_task = PythonOperator(
        task_id='clean_json_task',
        python_callable=clean_json,
        provide_context=True,
        op_args=['{{ ti.xcom_pull(task_ids="get_file_name") }}'],
    )

    bulk_load_task = PythonOperator(
        task_id='bulk_load_task',
        python_callable=bulk_load,
        provide_context=True,
    )

    start >> get_file_name_task >> clean_json_task >> bulk_load_task
