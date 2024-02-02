from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('pool_task', description='task_pool', schedule_interval=None,
          start_date=datetime(2024, 2, 1), catchup=False)

task1 = BashOperator(task_id='task_pool1',
                     bash_command='sleep 1', dag=dag, pool='my_pool')
task2 = BashOperator(task_id='task_pool2',
                     bash_command='sleep 1', dag=dag, pool='my_pool',
                     priority_weight=2)
task3 = BashOperator(task_id='task_pool3',
                     bash_command='sleep 1', dag=dag, pool='my_pool')
task4 = BashOperator(task_id='task_pool4',
                     bash_command='sleep 1', dag=dag, pool='my_pool',
                     priority_weight=10)
