from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


dag = DAG('python_task', description='Its dag extract data from S3', schedule_interval=None,
          start_date=datetime(2024,1,16), catchup=False)


def task_write(**kwargs):
    kwargs['ti'].xcom_push(key='valorxcom1', value=10200)    


def task_read(**kwargs):
    valor = kwargs['ti'].xcom_pull(key='valorxcom1')
    print(f'valor recuperado!! {valor}')


task1 = PythonOperator(task_id='task_extract1',python_callable=task_write , dag=dag)
task2 = PythonOperator(task_id='task_extract2',python_callable=task_read , dag=dag)


task1 >> task2