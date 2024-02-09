from airflow import DAG
from airflow import Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime
import pandas as pd

meu_dataset = Dataset("/opt/airflow/data/Churn_new.csv")


dag = DAG('consumer', description='consumer', schedule=[meu_dataset],
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


def meu_arquivo_transform():
    dataset = pd.read_csv("/opt/airflow/data/Churn_new.csv", sep=';')
    dataset.to_csv("/opt/airflow/data/Churn_new_dag.csv", sep=';')


verify_task = PythonOperator(task_id='verify_task', python_callable=meu_arquivo_transform,
                             dag=dag, provide_context=True)

verify_task