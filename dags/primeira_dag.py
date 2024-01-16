from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('extract_data', description='Its dag extract data from S3', schedule_interval=None,
          start_date=datetime(2024,1,16), catchup=False)

task1 = BashOperator(task_id='task_extract1', bash_command='sleep 5', dag=dag)
task2 = BashOperator(task_id='task_extract2', bash_command='sleep 5', dag=dag)
task3 = BashOperator(task_id='task_extract3', bash_command='sleep 5', dag=dag)

task1 >> task2 >> task3