
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






# Grupo de Tarefas (Task Group)
BR

*As tasks podem também serem executadas em grupos, para que precisemos de uma economia de tempo um pouco maior e não seja necessário executá-las separadamente. 
Para isso, devemos usar o tsk_group na parte de precedência.*

US

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



