
# **Prerequisites for Airflow Usage:**

- Docker Installation
- Installation of an IDE (Anaconda/VSCode)
- Airflow Installation with Docker

### Installing Airflow in the Environment:
1.	**Create a folder of your preference with the name "airflow"**

2.	**Save the following files in the folder:**

	- docker-compose.yaml (create a file in VSCode with this name)
		-	[docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml)
	- **.env** (with the following lines written):
		- AIRFLOW_IMAGE_NAME=apache/airflow:2.5.1
		- AIRFLOW_UID=50000

3.	**Follow the steps below:**

	- In the terminal, use the cd command to navigate to the path of the "airflow" folder where the above files are located, and execute the following commands:
		- `docker-compose up -d`
		- `docker-compose ps`  (checking the health of Docker)

4.	**Open your browser and go to localhost:8080**

	- The Airflow manager will be displayed:
		-	Username: airflow
		-	Password: airflow

Organize this text to make it visually appealing in the GitHub README.






## Task Group

*Tasks can also be executed in groups, allowing for a slightly greater time efficiency, and they do not need to be executed separately. 
To achieve this, we should use tsk_group in the dependency section.*



```python


from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.utils.task_group import TaskGroup

# Define the DAG
dag = DAG('dag_group', description='Esta task executa mais tasks', schedule_interval=None,
          start_date=datetime(2024, 1, 23), catchup=False)

# Define individual tasks
task1 = BashOperator(task_id='task1_exec', bash_command='sleep 2', dag=dag)
task2 = BashOperator(task_id='task2_exec', bash_command='sleep 3', dag=dag)
task3 = BashOperator(task_id='task3_exec', bash_command='sleep 3', dag=dag)
task4 = BashOperator(task_id='task4_exec', bash_command='sleep 3', dag=dag)
task5 = BashOperator(task_id='task5_exec', bash_command='sleep 3', dag=dag)
task6 = BashOperator(task_id='task6_exec', bash_command='sleep 3', dag=dag)

# Create a TaskGroup named 'Tks_group'
tsk_group = TaskGroup('Tks_group', dag=dag)

# Assign tasks to the TaskGroup
task7 = BashOperator(task_id='task7_exec', bash_command='sleep 3', dag=dag, task_group=tsk_group)
task8 = BashOperator(task_id='task8_exec', bash_command='sleep 3', dag=dag, task_group=tsk_group)
task9 = BashOperator(task_id='task9_exec', bash_command='sleep 3', dag=dag, task_group=tsk_group)

# Set up task dependencies
task1 >> task2
task3 >> task4
[task2, task4] >> task5 >> task6
task6 >> tsk_group  # task6 is set to run before the TaskGroup

# The DAG is now ready to be executed based on the defined dependencies and schedule.
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



