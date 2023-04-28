"""
Extract, transform and load of Foods's datamart.
Sources: USDA API
"""
from airflow import DAG
import datetime as dt
from transform.etl import extract, transform, load


default_args = {
    'depends_on_past' : False,
    'owner': 'me',
    'start_date': dt.datetime(2023, 4, 12), 
    'retries': 1,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay': dt.timedelta(minutes=60)
}

with DAG(
    'af_foods', 
    default_args=default_args,
    description='Foods and Nutrients ETL',
    schedule_interval=None,
) as dag:
    data = extract()
    processed_data = transform(data)
    load(processed_data)

