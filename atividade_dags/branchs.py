from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime
import pandas as pd
import statistics as sts


dag = DAG('Python_trated_data', description='Esta dag é para limpeza de dados e organização dos dados',
          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)


def clean_data():
    dataset = pd.read_csv('/opt/Airflow/data/Churn.csv', sep=';')
    dataset.columns = ['Id', 'Score', 'Estado', 'Genero', 'Idade', 'Patrimonio',
                       'Saldo', 'Produtos', "TemCartCred", 'Ativo', 'Salario', 'Saiu']

    mediana = sts.median(dataset['Salario'])
    """Atualizando dataset - se o valor do inplace não for True a alteração não é feita no próprio dataset, 
    apenas mostra como seria a modificação"""
    dataset['Salario'].fillna(mediana, inplace=True)

    dataset['Genero'].fillna('Masculino', inplace=True)

    mediana_idade = sts.median(dataset['Idade'])

    dataset['Idade'].fillna(mediana_idade, inplace=True)
    dataset.loc[(dataset['Idade'] < 0) | dataset['Idade']
                > 120, 'Idade'] = mediana_idade

    # Removendo duplicados e mantendo o primeiro valor com id
    dataset.drop_duplicates(subset='Id', keep='first', inplace=True)

    # Index = False, faz com que não se preocupe com o índice
    dataset.to_csv('/opt/Airflow/data/Churn_new.csv', sep=';', index=False)


t1 = PythonOperator(task_id='Execute_ETL', python_callable=clean_data, dag=dag)
