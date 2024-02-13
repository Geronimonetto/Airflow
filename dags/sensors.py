from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, date
from airflow.providers.http.sensors.http import HttpSensor
import requests


dag = DAG('sensors_api', description='Esta dag verifica a api', schedule_interval=None,
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


def query_api():
    response = requests.get("https://api.publicapis.org/entries")
    print(response.text)


verify_api = HttpSensor(task_id='verify_api',
                        http_conn_id='conexao_api', endpoint='entries',
                        poke_interval=5,
                        timeout=20,
                        dag=dag)
call_api = PythonOperator(
    task_id='call_api', python_callable=query_api, dag=dag)


verify_api >> call_api