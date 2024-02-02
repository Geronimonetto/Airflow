from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import random


dag = DAG('branch_teste', description='dag para teste de branch', schedule_interval=None,
          start_date=datetime(2024, 2, 1), catchup=False)


def gera_numero_aleatorio():
    return random.randint(1, 100)


gera_numero_alet = PythonOperator(
    task_id='gera_aleatorio', python_callable=gera_numero_aleatorio, dag=dag)


def verify_number(**context):
    number = context['task_instance'].xcom_pull(task_ids='gera_aleatorio')
    if number % 2 == 0:
        return 'par_task'
    else:
        return 'impar_task'


branch_task = BranchPythonOperator(
    task_id='verify_branch_task', python_callable=verify_number,
    provide_context=True,
    dag=dag)

par_task = BashOperator(
    task_id='par_task', bash_command='echo "Numero Par"', dag=dag)

impar_task = BashOperator(task_id='impar_task',
                          bash_command='echo "Numero Impar"', dag=dag)


gera_numero_alet >> branch_task
branch_task >> par_task
branch_task >> impar_task
