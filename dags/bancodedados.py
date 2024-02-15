from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, date


dag = DAG('postgre_dag', description='A Dag executa comandos SQL no banco de dados postgres', schedule_interval=None,
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


def print_result_db(ti):
    task_instance = ti.xcom_pull(task_ids='query_data')
    print("Resultado da consulta: ")
    for row in task_instance:
        print(row)


create_table = PostgresOperator(task_id='create_table',
                                postgres_conn_id='postgres_connect',
                                sql='create table if not exists teste(id int);',
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data',
                               postgres_conn_id='postgres_connect',
                               sql='insert into teste values(1);',
                               dag=dag)

query_data = PostgresOperator(task_id='query_data',
                              postgres_conn_id='postgres_connect',
                              sql='select * from teste;',
                              dag=dag,
                              do_xcom_push=True)

print_result = PythonOperator(task_id='print_result',
                              python_callable=print_result_db,
                              provide_context=True,
                              dag=dag)


create_table >> insert_data >> query_data >> print_result
