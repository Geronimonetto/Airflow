from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator


dag = DAG('task_dummy', description='Esta dag será uma dag teste para uma task dummy', schedule_interval=None,
          start_date=datetime(2024, 1, 31), catchup=False)

task1 = BashOperator(task_id="dummy1", bash_command='sleep 1', dag=dag)
task2 = BashOperator(task_id="dummy2", bash_command='sleep 1', dag=dag)
task3 = BashOperator(task_id="dummy3", bash_command='sleep 1', dag=dag)
task4 = BashOperator(task_id="dummy4", bash_command='sleep 1', dag=dag)
task5 = BashOperator(task_id="dummy5", bash_command='sleep 1', dag=dag)
task_dummy = DummyOperator(task_id='task_dummy', dag=dag)


[task1, task2, task3] >> task_dummy >> [task4, task5]
