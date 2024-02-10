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

```
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



