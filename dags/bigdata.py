from airflow import DAG
from airflow import Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime
from big_data_operator import BigDataOperator
import pandas as pd


dag = DAG('customer_csv', description='customer_csv', schedule=[meu_dataset],
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


customer_task = BigDataOperator(task_id='customer_task', path_to_csv_file='/opt/airflow/data/Churn.csv',
                                path_to_save_file='/opt/airflow/data/Churn.json', separator=';', file_type='json', dag=dag)


customer_task
