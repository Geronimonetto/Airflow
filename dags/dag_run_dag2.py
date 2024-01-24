from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime



dag = DAG('dag_run_2', description = 'Está dag é um exemplo de dag rodando dag', schedule_interval = None,
          start_date = datetime(2024,1,24), catchup= False)

task1 = BashOperator(task_id = 'task1_exec', bash_command= 'sleep 5', dag = dag)
task2 = TriggerDagRunOperator(task_id = 'task1_exec2', trigger_dag_id='dag_run_dag', dag = dag)

