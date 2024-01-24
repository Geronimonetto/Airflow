from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.utils.task_group import TaskGroup

dag = DAG('dag_group', description='Esta task executa mais tasks', schedule_interval = None, 
          start_date = datetime(2024,1,23), catchup=False)

task1 = BashOperator(task_id='task1_exec', bash_command='sleep 2', dag=dag) 
task2 = BashOperator(task_id='task2_exec', bash_command='sleep 3', dag=dag)
task3 = BashOperator(task_id='task3_exec', bash_command='sleep 3', dag=dag)
task4 = BashOperator(task_id='task4_exec', bash_command='sleep 3', dag=dag)
task5 = BashOperator(task_id='task5_exec', bash_command='sleep 3', dag=dag)
task6 = BashOperator(task_id='task6_exec', bash_command='sleep 3', dag=dag)

tsk_group = TaskGroup('Tks_group', dag=dag)

task7 = BashOperator(task_id='task7_exec', bash_command='sleep 3', dag=dag, task_group = tsk_group)
task8 = BashOperator(task_id='task8_exec', bash_command='sleep 3', dag=dag, task_group = tsk_group)
task9 = BashOperator(task_id='task9_exec', bash_command='sleep 3', dag=dag, task_group = tsk_group)

task1 >> task2
task3 >> task4
[task2, task4] >> task5 >> task6 
task6 >> tsk_group