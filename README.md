# Airflow
## Error docker desktop - unexpected wsl error
Vale lembrar que o erro que aconteceu no meu Docker pode ser diferente do que você encontre no seu computador.

- Abra o Powershell em modo administrador
- Escreva o seguinte comando
```
bcdedit /set HypervisorLaunchType auto
```
- Reinicie o computador
- Entre na BIOS do seu computador
- Verifique a opção Virtualization Technology está ativada
	- Desative e ative novamente
	- F10 para salvar
- Rode o Docker Desktop e veja se o problema persiste

## Instalação Airflow
**Para o uso do Airflow é necessário alguns pré-requisitos:**

- Instalação do Docker
- Instalação de alguma IDE (Anaconda/VSCode)
- Instalação do Airflow com Docker

### **Instalação do Airflow no ambiente:**

1. **Crie uma pasta de preferência com nome "airflow"**

2. **Salve os seguintes arquivos na pasta**
	- **docker-compose.yaml** (crie um arquivo no vscode com esse nome)
 	- copie tudo deste link para o arquivo docker-compose.yaml e salve dentro da pasta Airflow	
		- https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml
	- **.env** (com as seguintes linhas escritas)
		- AIRFLOW_IMAGE_NAME=apache/airflow:2.5.1
		- AIRFLOW_UID=50000
	
3. **Siga os procedimentos abaixo**
	- Com o terminal usando o comando cd, encontre o caminho da pasta airflow onde estão os arquivos acima e use os comandos abaixo:
		- `docker-compose up -d`
		- `docker-compose ps` (verificando a saúde do docker)

4. **Digite no seu navegador localhost:8080**
	- Aparecerá o o gerenciador do airflow:
		- Usuário: airflow
		- Senha: airflow

## **DAG's** 

- Contém nomes únicos 
- Podem ser separadas por classificação e departamento
- As DAGS devem ser agendadas
- Uma DAG é composta por uma ou mais Tasks

Sinônimo de DAG - Workflow ou Pipeline de orquestração de processamento de dados
- DAG é feita em Python (Arquivo python)
- .py - Extensão das Dags
- Por quesito de organização é padrão ter 1 Dag em cada arquivo .py (mas é possível colocar mais de 1 dag)

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import date, datetime

dag= DAG('dag_example', description='dag teste para execução', schedule_interval = None,
	start_date= datetime(date.today().year, date.today().month, date.today().day, catchup = False)

task_test1 = BashOperator(task_id='task1', bash_command='sleep 1', dag=dag)
task_test2 = BashOperator(task_id='task2', bash_command='sleep 1', dag=dag)

task1 >> task2

```
No exemplo acima podemos ver 2 tasks executando comando de bash(terminal) para esperar 1 segundo.

- Dag deve possuir o identificador único, no exemplo acima é o "exemplo_dag"
- Existem diversos tipos de operator - No exemplo acima é o BashOperator (Executam comando no shell do SO (sistema operacional))
- O identificador das tasks dentro da Dag devem ser únicos, bash_command - comando a ser executado (Sleep 5 (esperar 5 segundos)), dag - é um parâmetro obrigatório.
- Executando as tasks na ordem abaixo - task1 >> task2 >> task3

## Alterando configurações do Airflow
```yaml
AIRFLOW__CORE__FERNET_KEY: ''
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
AIRFLOW_API_AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
```
O Código acima está modificando a variável de ambiente para que os exemplos de Dags no Airflow não apareçam para não misturar com as Dags criadas pelo desenvolvedor, 
troque o 'true' de AIRFLOW__CORE__LOAD_EXAMPLES por 'false'
```yaml
AIRFLOW__CORE__FERNET_KEY: ''
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
AIRFLOW_API_AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
```
Adicione a linha abaixo para ver as configurações do Airflow (inteface)
```yaml
AIRFLOW__CORE__FERNET_KEY: ''
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
AIRFLOW_API_AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}

AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'true'
```
Adicione a linha abaixo - Para que o tempo de processamento de uma Dag após ser adicionada na pasta de Dags - O padrão do Airflow é 30.

```yaml
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}

AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'true'
AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL: 5
```
Adicione a linha abaixo - Por padrão o Airflow só busca uma nova Dag a cada 5 minutos (300 seg), logo alterando esse 
código o tempo de busca por novas Dags é de 20 segundos.

```yaml
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}

AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'true'
AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL: 5
AIRFLOW__CHEDULER__DAG_DIR_LIST_INTERVAL: 20
```
Após fazer essas modificações no docker-compose.yaml devemos parar o docker-compose
```bash
docker-compose down
```
e rodar novamente para atualizar
```bash
docker-compose up -d
```
## Execução em paralelo das tasks


Para que as tasks sejam executadas em paralelo devemos colocar as tasks em uma lista.

Exemplo: 

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, date


dag = DAG('example_dag', description='Descrição da dag', schedule_interval=None,
		 start_date=datetime(2024,10,2), catchup=False)


task_one = BashOperator(task_id='bash_task', bash_command='sleep 5', dag=dag)
task_two = BashOperator(task_id='bash_task2', bash_command='sleep 5', dag=dag)
task_three = BashOperator(task_id='bash_task3', bash_command='sleep 5', dag=dag)


task_one >> [task_two, task_three]

```


ao final do código podemos ver que a task1 será executada e após a finalização as tasks 2 e 3 serão executadas em paralelo.
Assim como para inverter a ordem de precedência basta modificar a lista para o início e a task a ser executada logo após.

Exemplo:

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, date


dag = DAG('example_dag', description='Descrição da dag', schedule_interval=None,
		 start_date=datetime(2024,10,2), catchup=False)


task_one = BashOperator(task_id='bash_task', bash_command='sleep 5', dag=dag)
task_two = BashOperator(task_id='bash_task2', bash_command='sleep 5', dag=dag)
task_three = BashOperator(task_id='bash_task3', bash_command='sleep 5', dag=dag)


[task_one,task_two] >> task_three

```

Usando funções no Python para execução de tasks
set_upstream - Seleciona qual task será executada depois da selecionada.

Exemplo:

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, date


dag = DAG('example_dag', description='Descrição da dag', schedule_interval=None,
		 start_date=datetime(2024,10,2), catchup=False)


task_one = BashOperator(task_id='bash_task', bash_command='sleep 5', dag=dag)
task_two = BashOperator(task_id='bash_task2', bash_command='sleep 5', dag=dag)
task_three = BashOperator(task_id='bash_task3', bash_command='sleep 5', dag=dag)


task_one.set_upstream(task_two)  # A task_one será executada após a task_two

```


## Task Group

As tasks podem também serem executadas em grupos, para que precisemos uma economia de tempo um pouco maior e não serão precisas executa-lás separadamente.

Para isso devemos usar o tskgroup na parte de precedência

```python
from airflow import DAG

from airflow.operators.bash_operator import BashOperator

from datetime import datetime

from airflow.utils.task_group import TaskGroup

  

dag = DAG('dag_group', description='Esta task executa mais tasks', schedule_interval = None,

          start_date = datetime(2024,1,23), catchup=False)

  

task1 = BashOperator(task_id='task1_exec', bash_command='sleep 2', dag=dag)

task2 = BashOperator(task_id='task2_exec', bash_command='sleep 3', dag=dag)

task3 = BashOperator(task_id='task3_exec', bash_command='sleep 3', dag=dag)

task4 = BashOperator(task_id='task4_exec', bash_command='sleep 3', dag=dag)

task5 = BashOperator(task_id='task5_exec', bash_command='sleep 3', dag=dag)

task6 = BashOperator(task_id='task6_exec', bash_command='sleep 3', dag=dag)

  

tsk_group = TaskGroup('Tks_group', dag=dag)  #Criando um grupo de tasks

  
#Informando que as tasks pertecem ao grupo

task7 = BashOperator(task_id='task7_exec', bash_command='sleep 3', dag=dag, task_group = tsk_group)  

task8 = BashOperator(task_id='task8_exec', bash_command='sleep 3', dag=dag, task_group = tsk_group)

task9 = BashOperator(task_id='task9_exec', bash_command='sleep 3', dag=dag, task_group = tsk_group)

  

task1 >> task2

task3 >> task4

[task2, task4] >> task5 >> task6

task6 >> tsk_group
```

## Send Email with Airflow 

If an error occurs in the DAG, Airflow automatically sends email notifications.

Another way is to create a task so that at the end of the pipeline, the task sends the email.

Automatic, definition in the DAG:

```python
email_on_failure = True  # (Sends email if a failure occurs)
email_on_retry = False  # (Sends email if the task is retried automatically)
retries = 1  # Defines the number of times a task will be retried before failing permanently
retry_delay = timedelta(minutes=5)  # Defines the time interval between retries
```

EmailOperator:

Sends an email within the Airflow workflow. What is needed for EmailOperator to work?

SMTP Server - Email service
Configure Airflow
Configuring G-MAIL:

Settings
Set a password for Airflow
Add the following lines to your docker-compose.yaml:

```yaml
AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
AIRFLOW__SMTP__SMTP_USER: your email
AIRFLOW__SMTP__SMTP_PASSWORD: generated password
AIRFLOW__SMTP__SMTP_PORT: 587
AIRFLOW__SMTP__MAIL_FROM: Airflow
```
## Xcom

o Xcom funciona para trocar dados entre tasks

**ti(task instance)** - é o objeto que representa a instância de tarefa sendo executada

**xcom_push()** - é usado para definir o valor
**xcom_pull()** - é usado para recuperar o valor

## Airflow Variables

Functionality for Sharing Information Between DAGs:

- API Credentials
- URLs
- Authentication Keys
- File Paths

Variables Creation Methods:
Variables can be created through the graphical interface, CLI, or Python script.

Difference between Variables and XCom:

Variables:

- Static and global information
- Used across the entire pipeline
XCom:

- Dynamic information
- Exchanged between tasks within the same DAG

*Creating Variables via Interface - Step 1: Admin >> Step 2: Variables*

Scope of Variables:

- Key: variable_name
- Value: random_information (example)
- Description: -

Once created in Airflow, this variable becomes global and can be called in Python. For instance, we create a variable named 'my_var' with the value 'hello'.

Example:

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime

dag = DAG('variables', description='Global Variables',
          schedule_interval=None, start_date=datetime(2024, 2, 1), catchup=False)

def print_variable(**context):
    my_var = Variable.get('my_var')
    print(f'The value of the variable is {my_var}')

task1 = PythonOperator(task_id='tsk1', python_callable=print_variable, dag=dag)

task1
#Result: The value of the variable is hello (Displayed in the DAG log)
```

## Branchs

Muito comum um pipeline precisar seguir em direções diferentes de acordo com resultado de eventos (Condições):
- Caminhos para dados válidos e inválidos
- Diferentes testes de qualidade
- Encaminhar diferentes e-mails conforme o resultado da análise
- etc

Operador - BranchPythonOperator (Built-in)

Exemplo:

Gerar número aleatório >> Branch >> Par ou Impar (2 tasks diferentes a serem executadas de acordo com a branch)

Exemplos de código de Branchs - O código executa uma função Python que gera um número aleatório inteiro, e podemos ver no exemplo as tasks usadas com o PythonOperator

```python
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

        return 'par_tasks'  # Deve ser a string com o nome da task_id

    else:

        return 'impar_tasks'  # O mesmo se repete aqui, deve-se por o nome do task_id

  
  

branch_task = BranchPythonOperator(

    task_id='recebe_numero_task', python_callable=recebe_numero, provide_context=True, dag=dag)

  

par_task = BashOperator(task_id='par_tasks',

                        bash_command='echo "Par"', dag=dag)

impar_task = BashOperator(task_id='impar_tasks',

                          bash_command='echo "impar"', dag=dag)

  
  

task_gera_numero >> branch_task

branch_task >> par_task

branch_task >> impar_task
```

## Dataset no Airflow


Dataset no airflow funciona de forma diferente, podendo ser alterado para execução de uma DAG ou task conforma a alteração de dataset, ou seja ao invés de fazer agendamento por tempo, podemos alterar para ser executado conforma o dataset é alterado.

Os datasets podem ser de diversos tipos, banco de dados, arquivo físico entre outros.

Dag Producer: Atualiza dados
Dag Consumer: schedule: Dataset - Parâmetro do Dag Consumer.

Exemplo: 

**DAG Producer**
```python

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
```

**DAG consumer**

```python
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
```
## Pools


São usado para gerenciar a concorrência e a alocação de recursos

Exemplo:
- Varias tarefas que precisam acessar um banco de dados
- Limites de conexões e recursos
- Você cria um pool que vai limitar e gerenciar o uso destas conexões

Primeiramente vamos criar uma DAG com 4 tasks paralelas
- Vamos rodar e ver como são executadas

Vamos criar 1 pool com 1 slot
- Slot = worker disponível para o recurso - onde as tasks são executadas - 1 Slot executa apenas 1 task por vez, mesmo com a opção de paralelismo.
- Dessa forma, o pool vai gerenciar o uso do worker

Vamos definir priority_weight para as tasks - maior será a prioridade dela no pool e serão executadas primeiro.

- Após a execução das tasks, elas são executadas ao mesmo momento.

Modificando pools na interface airflow:
- Passo 1 - Admin >> Pools
- Passo 2 - Crie um Pool
- Passo 3 - Nomeie o Pool - Digite o número de slots - Description (optional)
- Passo 4 - Modifique o código Python adicionando a variavel pool nas tasks

Example:

```python
from airflow import DAG

from airflow.operators.bash_operator import BashOperator

from datetime import datetime

  

dag = DAG('pool_task', description='task_pool', schedule_interval=None,

          start_date=datetime(2024, 2, 1), catchup=False)

  
# Por padrão o pool ja vem no BashOperator, então devemos adicionar apenas o nome da pool criada na interface do airflow

task1 = BashOperator(task_id='task_pool1', bash_command='sleep 1', dag=dag, pool = 'my_pool')

task2 = BashOperator(task_id='task_pool2', bash_command='sleep 1', dag=dag, pool = 'my_pool')

task3 = BashOperator(task_id='task_pool3', bash_command='sleep 1', dag=dag, pool = 'my_pool')

task4 = BashOperator(task_id='task_pool4', bash_command='sleep 1', dag=dag, pool = 'my_pool')
```

Aumentando a prioridade com **priority_weight** - Será executada de acordo com número da prioridade

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('pool_task', description='task_pool', schedule_interval=None,
          start_date=datetime(2024, 2, 1), catchup=False)

task1 = BashOperator(task_id='task_pool1',
                     bash_command='sleep 1', dag=dag, pool='my_pool')
task2 = BashOperator(task_id='task_pool2',
                     bash_command='sleep 1', dag=dag, pool='my_pool',
                     priority_weight=2)
task3 = BashOperator(task_id='task_pool3',
                     bash_command='sleep 1', dag=dag, pool='my_pool')
task4 = BashOperator(task_id='task_pool4',
                     bash_command='sleep 1', dag=dag, pool='my_pool',
                     priority_weight=10)


```
## Sensors

Os sensores aguardam um evento ou disponibilidade de um serviço, não executa nenhuma ação adicional.
Os sensores não fazem nada, quando o serviço estiver disponível ele chama a próxima task
Por exemplo: 
- Verifica arquivo e outra task importa 

Principais sensores: 

1.  **FileSensor**: Aguarda a existência ou a ausência de um arquivo em um caminho específico.
2.  **HttpSensor**: Aguarda a disponibilidade de uma URL
3. **S3KeySensor**: Aguarda a existência ou a ausência de uma chave em um bucket S3
4. **SqlSensor**: Aguarda a execução de uma consulta SQL em um banco de dados

Parâmetros:

1. **poke_interval:** Define o interval de tempo entre as verificações do sensor
2. timeout: Define o tempo máximo que o sensor pode esperar antes de atingir o tempo limite
3. **soft_fail:** Especifica se o sensor deve falhar silenciosamente (retornando "False") ou gerar uma exceção quando atinge o tempo limite.
4. **mode:** Especifica o modo de operação do sensor ("reschedule" para agendar novamente a tarefa ou "poke" para continuar verificando até que a condição seja atendida)
5. **poke_on_failure:** Especifica se o sensor deve continuar verificando quando ocorre uma falha na verificação anterior.

### Exemplo com HttpSensor 

1. Verificar a disponibilidade da API
	- https://api.publicapis.org/entries
	- Esta API é uma lista de APIs publicas
2. Um PythonOperator vai consultar a API caso disponível
3. Precisamos cadastrar a API como uma conexão.

#### Passo a Passo

- Crie uma conexão no airflow
- connection id: Nome da variavel a ser usada no Python
- connection Type: Http
- Host: API ( https://api.publicapis.org/) - *A ultima barra deve ser mantida para funcionar o endpoint*
- Concluido

```python
from airflow import DAG

from airflow.operators.python_operator import PythonOperator

from datetime import datetime, date

from airflow.providers.http.sensors.http import HttpSensor

import requests

  
  

dag = DAG('sensors_api', description='Esta dag verifica a api', schedule_interval=None,

          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)

  
  
# Função que chama a API e seu resultado
def query_api():

    response = requests.get("https://api.publicapis.org/entries")

    print(response.text)

  
  
# Task para verificar se a API está disponível
verify_api = HttpSensor(task_id='verify_api',

                        http_conn_id='conexao_api', endpoint='entries',

                        poke_interval=5,

                        timeout=20,

                        dag=dag)
                       
# Task para chamar a função que chama a API
call_api = PythonOperator(

    task_id='call_api', python_callable=query_api, dag=dag)

  
  

verify_api >> call_api
```

## Providers

São módulos Python que estendem a funcionalidade do airflow

Existem vários tipos: operators, sensors, hooks e outros.

Muitos já fazem parte do Airflow

Podem ser instalados usando PIP

Exemplos:
	- apache-airflow-providers-postgres
	- apache-airflow-providers-amazon
	- apache-airflow-providers-google

Utilizaremos o apache-airflow-providers-postgres para interação com o banco de dados

Exercício:


$$
Criar uma tabela ==> Inserir um dados ==> Consultar a tabela ==> Imprimir o resultado
$$


### Passo a Passo

Verifique a lista de providers em admin > providers para saber se o provider que você quer utilizar ja vem pré-instalado 

alguns exemplos:
	- apache-airflow-providers-amazon --> Amazon Integration
	- apache-airflow-providers-elasticsearch --> Elasticsearch

#### Criando a conexão
**conecct_id** - indique o nome (postgres_connect - nosso exemplo)
**host** - postgres
**connection_type** - postgres


Acompanhe o código para criação - inserção e consulta no banco de dados

```python
from airflow import DAG

from airflow.providers.postgres.operators.postgres import PostgresOperator

from airflow.operators.python_operator import PythonOperator

from datetime import datetime, date

  
  
# Criando DAG
dag = DAG('postgre_dag', description='A Dag executa comandos SQL no banco de dados postgres', schedule_interval=None,

          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)

  
  
# Função para imprimir dados contidos na tabela
def print_result_db(ti):

    task_instance = ti.xcom_pull(task_ids='query_data')

    print("Resultado da consulta: ")

    for row in task_instance:

        print(row)

  
  
# Task para criar uma tabela
create_table = PostgresOperator(task_id='create_table',

                                postgres_conn_id='postgres_connect',

                                sql='create table if not exists teste(id int);',

                                dag=dag)

  
# Task para inserir dados na tabela
insert_data = PostgresOperator(task_id='insert_data',

                               postgres_conn_id='postgres_connect',

                               sql='insert into teste values(1);',

                               dag=dag)

  
# Task para consultar dados da tabela
query_data = PostgresOperator(task_id='query_data',

                              postgres_conn_id='postgres_connect',

                              sql='select * from teste;',

                              dag=dag,

                              do_xcom_push=True)

  
# Task para imprimir valor da tabela no banco de dados
print_result = PythonOperator(task_id='print_result',

                              python_callable=print_result_db,

                              provide_context=True,

                              dag=dag)

  
  

create_table >> insert_data >> query_data >> print_result
```

## Hooks

São componentes para interagir com componentes do ambiente externo

Por que usar os hooks ao invés dos providers?

- São mais complexos porém são mais flexíveis

São classes que podem ser instanciadas

PostgresOperator - Encapsula o PostgresHook com pouquíssimo código


Exercício:

Mesmo exemplo acima porém utilizando de forma diferente com hooks.

Diferentemente dos providers os hooks necessitam de funções ao invés de usar as tasks, por que diferente dos providers os hooks são usados em instâncias.

Exemplo de código:

```python
from airflow import DAG

from airflow.operators.python_operator import PythonOperator

from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import date, datetime

  
  

dag = DAG('hooks_postgres', description='hooks para postgres', schedule_interval=None,

          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)

  
  
# Função para criar tabela, usando a classe PostgresHook
def create_table():

    postgres_hook = PostgresHook(postgres_conn_id='postgres_connect')

    postgres_hook.run(

        'create table if not exists tabela_teste(id int);', autocommit=True)

  
  
# Função para inserir dados
def insert_data():

    postgres_hook = PostgresHook(postgres_conn_id='postgres_connect')

    postgres_hook.run('insert into tabela_teste values(20);', autocommit=True)

  
  
# Função para selecionar dados
def select_data(**context):

    postgres_hook = PostgresHook(postgres_conn_id='postgres_connect')

    records = postgres_hook.get_records('select * from tabela_teste;')

    context['ti'].xcom_push(key='query_data', value=records)

  
  
# Função para imprimir dados
def print_data(ti):

    task_instance = ti.xcom_pull(

        key='query_data', task_ids='select_table_task')

    print('dados da tabela:')

    for row in task_instance:

        print(row)

  
  
# Task para chamar a função create_data
create_table_task = PythonOperator(

    task_id='create_table_task', python_callable=create_table, dag=dag)

# Task para chamar a função insert_data
insert_table_task = PythonOperator(

    task_id='insert_table_task', python_callable=insert_data, dag=dag)

# Task para chamar a função select_data
select_table_task = PythonOperator(

    task_id='select_table_task', python_callable=select_data, provide_context=True, dag=dag)

# Task para imprimir os dados da tabela chamando a função print data
print_table_task = PythonOperator(

    task_id='print_table_task', python_callable=print_data, provide_context=True, dag=dag)

  
  

create_table_task >> insert_table_task >> select_table_task >> print_table_task
```

## CLI 

Comando usados no CLI do airflow, para que isso venha a funcionar devemos usar os seguintes comandos:

1. Verifique os containers do airflow - **docker ps**
2. Copie o segundo container  e use o comando - **docker exec -it nome-do-container**

*Podemos então verificar alguns comandos usados no airflow:*

* **airflow dags list** - verifica as listas de dags
* **airflow dags report** - mostra as 
	* dags existentes (nomes de arquivos)
	* duração 
	* numero de dags
	* numero de tasks
	* nome das dags
* **airflow dags list-jobs** 
	* Mostra informações das dags detalhadas
* **airflow dags next-execution nome-da-dag** 
	* Mostra se existe um agendamento para a dag
* **airflow dags list-runs -d nome-da-dag**
	* mostra a ultima execução feita pela dag
* **airflow dags pause nome-da-dag**
	* pausando dag
* **airflow dags unpause nome-da-dag 
	* despausando dag
* **airflow dags trigger nome-da-dag**
	* rodando dag
* **airflow tasks list nome-da-dag**
	* verificando a lista de tasks da dag
* **airflow tasks test nome-da-dag nome-da-task data-para-execução**
	* testando task de dag
* **airflow config list**
	* listando configurações
 * **airflow pools list**
	 * Mostrando lista de pools
* **airflow variables list**
	* listando variáveis do airflow
* **airflow cheat-sheet**
	* mostrando todos os comandos do airflow

***Miscellaneous commands***
* **airflow cheat-sheet**                       
	* Display cheat sheet
* **airflow dag-processor**                     
	* Start a standalone Dag Processor instance
* **airflow info**                              
	* Show information about current Airflow and environment
* **airflow kerberos**                          
	* Start a kerberos ticket renewer
* **airflow plugins**                           
	* Dump information about loaded plugins
* **airflow rotate-fernet-key**                 
	* Rotate encrypted connection credentials and variables
* **airflow scheduler**                         
	* Start a scheduler instance
* **airflow standalone**                        
	* Run an all-in-one copy of Airflow
* **airflow sync-perm**                         
	* Update permissions for existing roles and optionally DAGs
* **airflow triggerer**                         
	* Start a triggerer instance
* **airflow version**                           
	* Show the version
* **airflow webserver**                         
	* Start a Airflow webserver instance

***Celery components***
* **airflow celery flower**                     
	* Start a Celery Flower
* **airflow celery stop**                       
	* Stop the Celery worker gracefully
* **airflow celery worker**                     
	* Start a Celery worker node

***View configuration***
* **airflow config get-value**                  
	* Print the value of the configuration
* **airflow config list**                       
	* List options for the configuration

***Manage connections***
* **airflow connections add**                   
	* Add a connection
* **airflow connections delete**                
	* Delete a connection
* **airflow connections export**                
	* Export all connections
* **airflow connections get**                   
	* Get a connection
* **airflow connections import**                
	* Import connections from a file
* **airflow connections list**                  
	* List connections

***Manage DAGs***
* **airflow dags backfill**                     
	* Run subsections of a DAG for a specified date range
* **airflow dags delete**                       
	* Delete all DB records related to the specified DAG
* **airflow dags list**                         
	* List all the DAGs
* **airflow dags list-import-errors**           
	* List all the DAGs that have import errors
* **airflow dags list-jobs**                    
	* List the jobs
* **airflow dags list-runs**                    
	* List DAG runs given a DAG id
* **airflow dags next-execution**               
	* Get the next execution datetimes of a DAG
* **airflow dags pause**                        
	* Pause a DAG
* **airflow dags report**                       
	* Show DagBag loading report
* **airflow dags reserialize**                  
	* Reserialize all DAGs by parsing the DagBag files
* **airflow dags show**                         
	* Displays DAG's tasks with their dependencies
* **airflow dags show-dependencies**            
	* Displays DAGs with their dependencies
* **airflow dags state**                        
	* Get the status of a dag run
* **airflow dags test**                         
	* Execute one single DagRun
* **airflow dags trigger**                      
	* Trigger a DAG run
* **airflow dags unpause**                      
	* Resume a paused DAG

***Database operations***
* **airflow db check**                         
	* Check if the database can be reached
* **airflow db check-migrations**               
	* Check if migration have finished
* **airflow db clean**                         
	* Purge old records in metastore tables
* **airflow db downgrade**                     
	* Downgrade the schema of the metadata database.
* **airflow db init**                          
	* Initialize the metadata database
* **airflow db reset**                         
	* Burn down and rebuild the metadata database
* **airflow db shell**                         
	* Runs a shell to access the database
* **airflow db upgrade**                       
	* Upgrade the metadata database to latest version

***Manage jobs***
* **airflow jobs check**                       
	* Checks if job(s) are still alive

***Tools to help run the KubernetesExecutor***
* **airflow kubernetes cleanup-pods**          
	* Clean up Kubernetes pods (created by KubernetesExecutor/KubernetesPodOperator) in evicted/failed/succeeded/pending states
* **airflow kubernetes generate-dag-yaml**     
	* Generate YAML files for all tasks in DAG. Useful for debugging tasks without launching into a cluster

***Manage pools***
* **airflow pools delete**                     
	* Delete pool
* **airflow pools export**                     
	* Export all pools
* **airflow pools get**                        
	* Get pool size
* **airflow pools import**                     
	* Import pools
* **airflow pools list**                       
	* List pools
* **airflow pools set**                        
	* Configure pool

***Display providers***
* **airflow providers auth**                    
	* Get information about API auth backends provided
* **airflow providers behaviours**              
	* Get information about registered connection types with custom behaviours
* **airflow providers get**                     
	* Get detailed information about a provider
* **airflow providers hooks**                   
	* List registered provider hooks
* **airflow providers links**                   
	* List extra links registered by the providers
* **airflow providers list**                    
	* List installed providers
* **airflow providers logging**                 
	* Get information about task logging handlers provided
* **airflow providers secrets**                 
	* Get information about secrets backends provided
* **airflow providers widgets**                 
	* Get information about registered connection form widgets

***Manage roles***
* **airflow roles add-perms**                   
	* Add roles permissions
* **airflow roles create**                      
	* Create role
* **airflow roles del-perms**                   
	* Delete roles permissions
* **airflow roles delete**                      
	* Delete role
* **airflow roles export**                      
	* Export roles (without permissions) from db to JSON file
* **airflow roles import**                      
	* Import roles (without permissions) from JSON file to db
* **airflow roles list**                        
	* List roles

***Manage tasks***
* **airflow tasks clear**                       
	* Clear a set of task instance, as if they never ran
* **airflow tasks failed-deps**                 
	* Returns the unmet dependencies for a task instance
* **airflow tasks list**                        
	* List the tasks within a DAG
* **airflow tasks render**                      
	* Render a task instance's template(s)
* **airflow tasks run**                         
	* Run a single task instance
* **airflow tasks state**                       
	* Get the status of a task instance
* **airflow tasks states-for-dag-run**          
	* Get the status of all task instances in a dag run
* **airflow tasks test**                        
	* Test a task instance

***Manage users***
* **airflow users add-role**                    
	* Add role to a user
* **airflow users create**                      
	* Create a user
* **airflow users delete**                      
	* Delete a user
* **airflow users export**                     
	* Export all users
* **airflow users import**                      
	* Import users
* **airflow users list**                        
	* List users
* **airflow users remove-role **                
	* Remove role from a user

***Manage variables***
* **airflow variables delete**                   
	* Delete variable
* **airflow variables export**                  
	* Export all variables
* **airflow variables get**                     
	* Get variable
* **airflow variables import**                  
	* Import variables
* **airflow variables list**                    
	* List variables
* **airflow variables set**                     
	* Set variable

## Configurações do Airflow

Quando executamos o airflow no container existem 2 arquivos essenciais que existem

	Arquivo airflow.cfg
	docker-compose.yaml "Sobrescreve" o airflow.cfg

Airflow está dividido em seções de configurações:

	core - configurações mais importantes
	webserver - interface gráfica
	scheduler - serviço de agendamento

Usar variável de ambiente:
* Airflow__
* Seção__
* Configuração

Exemplo:

	smtp
	smtp_host = localhost
	
	AIRFLOW__SMTP__SMTP_HOST: 

#### Core

**dags_folder** = /path/to/your/dags/folder
	- *caminho das suas dags*
**base_log_folder** = /path/to/your/log/folder 
	- *caminho dos arquivos de log*
**executor** = SequentialExecutor
	- *Executer que está sendo usado*
**sql_alchemy_conn** = postgresql+psycopg2://user:password@localhost/db_name
	-  Onde estão os metadados
**parallelism** =32 - 
	- máximo de tasks que podem rodar em paralelo em todo o ambiente
**dag_concurrency** = 16
	-  número máximo de tarefas que podem ser executadas por dag

#### Webserver

- **web_server_host** = 0.0.0.0 - Endereço padrão
- **web_server_port** = 8080 - porta padrão
- **authenticate** = False - Se utiliza autenticação ou não

#### scheduler

- **scheduler_heartbeat_sec** = 5 
	- verifica se há alguma tarefa para ser executada
- **job_heartbeat_sec **= 5
	- frequência em segundos que verifica se o trabalho estã sendo executado corretamente
- **num_runs** = -1 
	- número de vezes que o scheduler executa antes de sair

#### Executers

	Alocação de recursos - como e onde executar tarefas
	Gerencia Paralelismo
	Gerencia Dependências
	Tratamento de falhas
	Monitora - as execuções
	Loga - registrar as execuções

##### Tipos de Executers

- **CeleryExecutor**==> Execução distribuída em cluster
- **SequentialExecutor** ==> Permite apenas execução sequencial
- **LocalExecuter** ==> Permite execução em paralelo, mas somente local
- **KubernetesExecutor** ==> Executa em ambientes Kubernetes

## Plugins

- Estende a funcionalidade do Airflow
- Pode encapsular código para reutilização
- Classe Python

Por padrão ja existe uma pasta para plugins

- Construtor que herda BaseOperator
- Precisa ter o método Execute 

##### Criando Plugins

O Plugin será para transformar arquivos csv em parquet ou JSON

#### Passo a Passo

Para a criação de um plugin devemos criar um arquivo python dentro da pasta plugins do airflow
e usar como base a classe BaseOperator do models


```python
from airflow.models import BaseOperator

from airflow.utils.decorators import apply_defaults

import pandas as pd

  
  
# Criando classe herdando do BaseOperator
class BigDataOperator(BaseOperator):

  

    @apply_defaults  # Utilizando o decorator
    def __init__(self, path_to_csv_file: str, path_to_save_file: str,

                 separator: str = ';', file_type: str = 'parquet', *args,

                 **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.path_to_csv_file: str = path_to_csv_file  # Caminho do arquivo

        self.path_to_save_file: str = path_to_save_file  # Caminho onde salva o arquivo

        self.separator: str = separator  # Separador do csv

        self.file_type: str = file_type  # Tipo do arquivo ex: csv, json

  
	# Criando função para executar a conversão do csv
    def execute(self, context: str) -> None:
		# lendo o arquivo csv
        df = pd.read_csv(self.path_to_csv_file, sep=self.separator)
		# Verificando o tipo do arquivo
        if self.file_type == 'parquet':

            df.to_parquet(self.path_to_save_file)
		
        elif self.file_type == 'json':

            df.to_json(self.path_to_save_file)
 
		# Tratamento de erro
        else:

            raise ValueError("O Tipo é Inválido!!")

```
Após a criação do plugin devemos criar uma dag para utilizar o nosso plugin.

```python
from airflow import DAG

from airflow import Dataset

from airflow.operators.python_operator import PythonOperator

from datetime import date, datetime

from big_data_operator import BigDataOperator  # Importando o plugin criado

import pandas as pd

  

dag = DAG('customer_csv', description='customer_csv', schedule=[meu_dataset],

          start_date=datetime(date.today().year, date.today().month, date.today().day), catchup=False)

  
  
# Criando uma task com o plugin criado e passando os parâmetros
customer_task = BigDataOperator(task_id='customer_task', path_to_csv_file='/opt/airflow/data/Churn.csv',

                                path_to_save_file='/opt/airflow/data/Churn.json', separator=';', file_type='json', dag=dag)

  
  

customer_task

```
