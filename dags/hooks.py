from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import date, datetime


dag = DAG('hooks_postgres', description='hooks para postgres', schedule_interval=None,
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


def create_table():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_connect')
    postgres_hook.run(
        'create table if not exists tabela_teste(id int);', autocommit=True)


def insert_data():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_connect')
    postgres_hook.run('insert into tabela_teste values(20);', autocommit=True)


def select_data(**context):
    postgres_hook = PostgresHook(postgres_conn_id='postgres_connect')
    records = postgres_hook.get_records('select * from tabela_teste;')
    context['ti'].xcom_push(key='query_data', value=records)


def print_data(ti):
    task_instance = ti.xcom_pull(
        key='query_data', task_ids='select_table_task')
    print('dados da tabela:')
    for row in task_instance:
        print(row)


create_table_task = PythonOperator(
    task_id='create_table_task', python_callable=create_table, dag=dag)
insert_table_task = PythonOperator(
    task_id='insert_table_task', python_callable=insert_data, dag=dag)
select_table_task = PythonOperator(
    task_id='select_table_task', python_callable=select_data, provide_context=True, dag=dag)
print_table_task = PythonOperator(
    task_id='print_table_task', python_callable=print_data, provide_context=True, dag=dag)


create_table_task >> insert_table_task >> select_table_task >> print_table_task
