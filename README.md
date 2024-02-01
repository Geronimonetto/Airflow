
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






# Task Group

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

# Send Email with Airflow 

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

## Variáveis do Airflow

Funcionam para o compartilhamento de informações entre as DAGS
	- Credenciais de API
	- URLs
	- Chaves de autenticação
	- Endereços de arquivos
As variáveis podem ser criadas através de Interface gráfica/ CLI / Python

Diferença entre variáveis e XCom

Variáveis:
- São informações estáticas e globais
- Usadas em todo o pipeline
XCom
- Informações dinâmicas
- Entre as tarefas - Informações trocadas na mesma DAG

Variáveis por interface - **Passo1** - Admin >> **Passo 2** - Variables
Escopo de variáveis

Key: nome_variavel
Val: informação_aleatoria (exemplo)
Description: -

Essa variável a partir da criação no Airflow será global podendo ser chamada no python, criamos uma variável chamada minha_var com o valor - ollá

Exemplo:

```
from airflow import DAG

from airflow.operators.python_operator import PythonOperator

from airflow.models import Variable

from datetime import datetime

  

dag = DAG('variaveis', description='Variaveis globais',

          schedule_interval=None, start_date=datetime(2024, 2, 1), catchup=False)

  
  

def print_variable(**context):

    minha_var = Variable.get('minha_var')

    print(f'O Valor da variável é {minha_var}')

  
  

task1 = PythonOperator(task_id='tsk1', python_callable=print_variable, dag=dag)

  

task1

#Result: O Valor da variável é ollá (Vemos isso no log da DAG)
```



