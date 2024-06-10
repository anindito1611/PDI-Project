from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook # type: ignore
import os

# Default arguments for the DAG
default_args = {
    'owner': 'data_engineer',
    'retries': 2,
    'retry_delay': timedelta(seconds=10),
}

def upload_files_to_cloud_storage():
    cloud_storage_path = '/opt/airflow/dags/source/'
    cloud_storage_bucket = 'airflow'
    cloud_storage_service = S3Hook(aws_conn_id='airflows3')

    for root, dirs, files in os.walk(cloud_storage_path):
        for file in files:
            file_to_upload = os.path.join(root, file)
            cloud_storage_key = os.path.relpath(file_to_upload, cloud_storage_path)
            cloud_storage_service.load_file(filename=file_to_upload, key=cloud_storage_key, bucket_name=cloud_storage_bucket, replace=True)

# Define the DAG
with DAG(
    dag_id='upload_files_to_cloud_storage_dag',
    default_args=default_args,
    description='A DAG to upload files from a folder to cloud storage',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    upload_task = PythonOperator(
        task_id='upload_files_to_cloud_storage_task',
        python_callable=upload_files_to_cloud_storage,
    )
