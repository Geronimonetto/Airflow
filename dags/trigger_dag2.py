from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, date


dag = DAG('exemplo_trigger2', description= 'Its dag is of very comprehension!', schedule_interval = None, start_date = datetime(2024, 1, 22), catchup=False)

task1 = BashOperator(task_id='extract_task1', bash_command='exit 1', dag=dag)
task2 = BashOperator(task_id='extract_task2', bash_command='sleep 5', dag=dag)
task3 = BashOperator(task_id='extract_task3', bash_command='sleep 5', dag=dag, trigger_rule='one_failed')

[task1, task2] >> task3 