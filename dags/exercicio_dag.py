from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('Exemplo_dag', description='Este é um exemplo de dag', schedule_interval='@hourly',
          start_date=datetime(2024, 1, 25), catchup=False)

task1 = BashOperator(task_id='task1_d', bash_command='sleep 5', dag=dag)
task2 = TriggerDagRunOperator(
    task_id='task_exec', trigger_dag_id='dag_run_dag2', dag=dag)
