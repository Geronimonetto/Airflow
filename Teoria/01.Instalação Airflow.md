
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

