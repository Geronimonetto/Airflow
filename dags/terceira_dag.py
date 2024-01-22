from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('extract_data_three', description='Its dag extract data from S3, and send for db2', schedule_interval=None,
          start_date=datetime(2024, 1, 22), catchup=False)

task1 = BashOperator(task_id='task_extract1', bash_command='sleep 5', dag=dag)
task2 = BashOperator(task_id='task_extract2', bash_command='sleep 5', dag=dag)
task3 = BashOperator(task_id='task_extract3', bash_command='sleep 5', dag=dag)

[task2,task3] >> task1
