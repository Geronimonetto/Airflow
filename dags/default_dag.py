from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False,
    'email': ['teste@teste.com'],
    'start_date': datetime(2024,1,24),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

dag = DAG('default_args_new', description='Dag de exemplo', 
          default_args = default_args,
          schedule_interval = '@hourly',
          default_view = 'graph',
          catchup=False,
          tags=['process','tag','pipeline'])


task1 = BashOperator(task_id='task_extract1', bash_command='sleep 5', dag= dag)
task2 = BashOperator(task_id='task_extract2', bash_command='sleep 5', dag= dag)
task3 = BashOperator(task_id='task_extract3', bash_command='sleep 5', dag= dag)

task1 >> task2 >> task3