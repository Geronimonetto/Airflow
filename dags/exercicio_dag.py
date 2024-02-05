from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime


dag = DAG('task_duummy_exercicio', description='This is task dummy, where we create a conection with parallel tasks', schedule_interval='@hourly',
          start_date=datetime(2024, 2, 1), catchup=False)

task1 = BashOperator(task_id='dummy_task_one', bash_command='sleep 2', dag=dag)
task2 = BashOperator(task_id='dummy_task_two', bash_command='sleep 2', dag=dag)
task3 = BashOperator(task_id='dummy_task_three',
                     bash_command='sleep 2', dag=dag)
task_connection = DummyOperator(task_id='Task_connection', dag=dag)
task_connection2 = DummyOperator(task_id='Task_connection2', dag=dag)
task4 = BashOperator(task_id='dummy_task_four',
                     bash_command='sleep 2', dag=dag)
task5 = BashOperator(task_id='dummy_task_five',
                     bash_command='sleep 2', dag=dag)
task6 = BashOperator(task_id='dummy_task_six',
                     bash_command='sleep 2', dag=dag)
task7 = BashOperator(task_id='dummy_task_seven',
                     bash_command='sleep 2', dag=dag)

[task1, task2]  >> task_connection >> [task3, task4] >> task_connection2
task_connection2 >> [task5, task6, task7]
