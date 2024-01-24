from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG('dag_run_dag', description='Esta task executa mais tasks', schedule_interval = None, 
          start_date = datetime(2024,1,23), catchup=False)

task1 = BashOperator(task_id='task1_exec', bash_command='sleep 2', dag=dag) 
task2 = BashOperator(task_id='task2_exec', bash_command='sleep 3', dag=dag)


task1 >> task2
