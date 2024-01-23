from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('Exemplo_dag3', description= 'Essa dag fica responsável para executar quando as outras falharem! all_failed', schedule_interval = None, 
          start_date = datetime(2024,1,23), catchup= False)


task1 = BashOperator(task_id= 'nova_task1', bash_command = 'exit 1', dag = dag)
task2 = BashOperator(task_id= 'nova_task2', bash_command = 'exit 1', dag = dag)
task3 = BashOperator(task_id= 'nova_task3', bash_command = 'sleep 2', dag = dag, trigger_rule= 'all_failed')

[task1, task2] >> task3

