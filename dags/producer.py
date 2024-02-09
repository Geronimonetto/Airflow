from airflow import DAG
from airflow import Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import date,datetime
import pandas as pd


dag = DAG('producer', description='producer',
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)

meu_dataset = Dataset("/opt/airflow/data/Churn_new.csv")


def meu_arquivo():
    dataset = pd.read_csv("/opt/airflow/data/Churn.csv", sep=';')
    dataset.to_csv("/opt/airflow/data/Churn_new.csv", sep=';')


verify_task = PythonOperator(task_id='verify_task', python_callable=meu_arquivo, dag=dag, outlets=[meu_dataset]) # outlets - informa que irá atualizar o dataset

verify_task