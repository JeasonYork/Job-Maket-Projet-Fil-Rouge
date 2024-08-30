from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import os
import shutil
import time
import glob

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'json_processing_pipeline_10',
    default_args=default_args,
    description='Pipeline to process new JSON files',
    schedule_interval=None,
)

JSON_TEMP_DIR = '/opt/airflow/ETL/Json_temp'
JSON_SCRAPING_DIR = '/opt/airflow/ETL/Json_scraping'
JSON_TRANSFORMED_DIR = '/opt/airflow/ETL/Json_transformed'

def is_file_stable(file_path, interval=5, timeout=60):
    initial_size = -1
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_size = os.path.getsize(file_path)
        if current_size == initial_size:
            return True
        initial_size = current_size
        time.sleep(interval)
    return False

def clean_json(file_path, **kwargs):
    import subprocess

    log_file = os.path.join('/opt/airflow/logs', f"{os.path.basename(file_path)}.log")

    if is_file_stable(file_path):
        # Run the Data_cleaning.py script
        subprocess.run(['python', '/opt/airflow/ETL/Transform/data_cleaning.py', file_path, JSON_TRANSFORMED_DIR, log_file], check=True)

        # Move original JSON file to Json_scraping
        shutil.move(file_path, os.path.join(JSON_SCRAPING_DIR, os.path.basename(file_path)))

        # Return the path of the transformed file
        transformed_file_path = os.path.join(JSON_TRANSFORMED_DIR, f"{os.path.splitext(os.path.basename(file_path))[0]}_updated.json")
        return transformed_file_path
    else:
        raise RuntimeError(f"File {file_path} is not stable.")

def list_new_json_files(**kwargs):
    file_list = glob.glob(os.path.join(JSON_TEMP_DIR, '*.json'))
    if file_list:
        return file_list  # Returning the list of files found
    else:
        raise ValueError("No JSON files found in the directory")

def process_files(**kwargs):
    ti = kwargs['ti']
    files = ti.xcom_pull(task_ids='list_new_json_files')
    if not files:
        raise ValueError("No files to process")

    transformed_files = []
    for file_path in files:
        transformed_file_path = clean_json(file_path=file_path)
        transformed_files.append(transformed_file_path)

    # Push the list of transformed files to XComs
    ti.xcom_push(key='transformed_files', value=transformed_files)

def bulk_load(**kwargs):
    import subprocess

    ti = kwargs['ti']
    transformed_files = ti.xcom_pull(key='transformed_files', task_ids='process_files')
    log_file = "/opt/airflow/logs/bulk_load_task.log"

    for file_path in transformed_files:
        # Run the Bulk_script.py script
        subprocess.run(['python', '/opt/airflow/ETL/Load/bulk_script_ft.py', file_path, log_file], check=True)

with dag:
    # Sensor to monitor new JSON files in the directory
    new_json_file_sensor = FileSensor(
        task_id='new_json_file_sensor',
        filepath=JSON_TEMP_DIR,
        fs_conn_id='fs_jobmarket',
        poke_interval=10,
        timeout=600,
        mode='reschedule',
    )

    # Task to list new JSON files
    list_new_json_files_task = PythonOperator(
        task_id='list_new_json_files',
        python_callable=list_new_json_files,
        provide_context=True,
    )

    # Task to process each JSON file found
    process_files_task = PythonOperator(
        task_id='process_files',
        python_callable=process_files,
        provide_context=True,
    )

    # Task to bulk load the cleaned JSON
    bulk_load_task = PythonOperator(
        task_id='bulk_load_task',
        python_callable=bulk_load,
        provide_context=True,
    )

    new_json_file_sensor >> list_new_json_files_task >> process_files_task >> bulk_load_task
