from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

with DAG('quarta_dag', description='Quarta DAG',
         schedule_interval=None, start_date=datetime(2024, 1, 22),
         catchup=False) as dag:

    task1 = BashOperator(task_id='task_extract1', bash_command='sleep 5')
    task2 = BashOperator(task_id='task_extract2', bash_command='sleep 5')
    task3 = BashOperator(task_id='task_extract3', bash_command='sleep 5')

    task1.set_upstream(task2)  # A task1 será executada após a task2
    task2.set_upstream(task3)  # A task será executada após a task3
