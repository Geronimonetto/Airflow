from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('exemplo_task4', description='Esta task executa mais tasks', schedule_interval = None, 
          start_date = datetime(2024,1,23), catchup=False)

task1 = BashOperator(task_id='task1_exec', bash_command='sleep 2', dag=dag) 
task2 = BashOperator(task_id='task2_exec', bash_command='sleep 3', dag=dag)
task3 = BashOperator(task_id='task3_exec', bash_command='sleep 3', dag=dag)
task4 = BashOperator(task_id='task4_exec', bash_command='sleep 3', dag=dag)
task5 = BashOperator(task_id='task5_exec', bash_command='sleep 3', dag=dag)
task6 = BashOperator(task_id='task6_exec', bash_command='sleep 3', dag=dag)
task7 = BashOperator(task_id='task7_exec', bash_command='sleep 3', dag=dag)
task8 = BashOperator(task_id='task8_exec', bash_command='sleep 3', dag=dag)
task9 = BashOperator(task_id='task9_exec', bash_command='sleep 3', dag=dag)

task1 >> task2
task3 >> task4
[task2, task4] >> task5 >> task6 
task6 >> [task7, task8, task9]