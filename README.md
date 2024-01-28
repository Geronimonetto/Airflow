
**Para o uso do Airflow é necessário alguns pré-requisitos:**

- Instalação do Docker
- Instalação de alguma IDE (Anaconda/VSCode)
- Instalação do Airflow com Docker

### **Instalação do Airflow no ambiente:**

1. **Crie uma pasta de preferência com nome "airflow"**

2. **Salve os seguintes arquivos na pasta**
	- **docker-compose.yaml** (crie um arquivo no vscode com esse nome)
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


- Sinônimo de DAG - Workflow ou Pipeline de orquestração de processamento de dados
- DAG é feita em Python (Arquivo python)
- .py - Extensão das Dags
- Por quesito de organização é padrão ter 1 Dag em cada arquivo .py (mas é possível colocar mais de 1 dag)

	![[Pasted image 20240116163342.png]]

- Dag deve possuir o identificador único, no exemplo acima é o "exemplo_dag"
- Existem diversos tipos de operator - No exemplo acima é o BashOperator (Executam comando no shell do SO (sistema operacional))
- O identificador das tasks dentro da Dag devem ser únicos, bash_command - comando a ser executado (Sleep 5 (esperar 5 segundos)), dag - é um parâmetro obrigatório.
- Executando as tasks na ordem abaixo - task1 >> task2 >> task3

![[Pasted image 20240116163818.png]]
Modificando a variável de ambiente para que os exemplos de Dags no Airflow não apareçam para não misturar com as Dags criadas pelo desenvolvedor, troque o 'true' por 'false'

Adicione a linha abaixo para ver as configurações do Airflow (inteface)

![[Pasted image 20240116164126.png]]

Adicione a linha abaixo - Para que o tempo de processamento de uma Dag após ser adicionada na pasta de Dags - O padrão do Airflow é 30.

![[Pasted image 20240116164355.png]]

Adicione a linha abaixo - Por padrão o Airflow só busca uma nova Dag a cada 5 minutos (300 seg), logo alterando esse código o tempo de busca por novas Dags é de 20 segundos.

![[Pasted image 20240116164615.png]]

Após fazer essas modificações no docker-compose.yaml devemos parar o docker-compose e novamente para atualizar - 

`docker-compose down` #Pausandodocker

![[Pasted image 20240116165017.png]]

`docker-compose up -d`  #Rodandodocker

![[Pasted image 20240116165142.png]]

