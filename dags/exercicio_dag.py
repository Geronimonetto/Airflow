from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, date
from airflow.operators.python_operator import BranchPythonOperator
from random import randint

dag = DAG('Dag_example', description='Está dag é um exemplo de branch', schedule_interval=None,
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


def gera_numero() -> int:
    return randint(1, 1000)


task_gera_numero = PythonOperator(
    task_id='task_gerador', python_callable=gera_numero, dag=dag)


def recebe_numero(**args):
    numero = args['task_instance'].xcom_pull(task_ids='task_gerador')

    if numero % 2 == 0:
        return 'par_tasks'  # Deve ser a string com o nome da task_id
    else:
        return 'impar_tasks'  # O mesmo se repete aqui, deve-se por o nome do task_id


branch_task = BranchPythonOperator(
    task_id='recebe_numero_task', python_callable=recebe_numero, provide_context=True, dag=dag)

par_task = BashOperator(task_id='par_tasks',
                        bash_command='echo "Par"', dag=dag)
impar_task = BashOperator(task_id='impar_tasks',
                          bash_command='echo "impar"', dag=dag)


task_gera_numero >> branch_task
branch_task >> par_task
branch_task >> impar_task
