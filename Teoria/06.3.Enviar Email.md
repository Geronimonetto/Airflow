Caso ocorra algum erro na DAG, o Airflow envia notificações automáticas via e-mail informando.

Outra forma é criar uma task para que ao fim da pipeline a task envia o e-mail;
- Automático, definição na DAG
	- **email_on_failure** = True - (Envia e-mail caso ocorra uma falha)
	- **email_on_retry** = False - (Envia e-mail caso a tarefa seja executada automaticamente)
	- **retries** = 1 - Isso define o número de vezes que uma tarefa será reprocessada antes de falhar definitivamente
	- **retry_delay** = timedelta(minutes=5) - Isso define o intervalo de tempo entre os reprocessamento
- **EmailOperator**
	- Envia um email dentro do fluxo do Airflow
- *O que é preciso para o EmailOperator funcionar?*
	- Servidor SMTP - Serviço de e-mail
	- Configurar o Airflow

- Configurando o G-MAIL 
	- Configurações
	- Configure uma senha para o Airflow

- Adicione as seguintes linhas no seu docker-compose.yaml
	- AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
	- AIRFLOW__SMTP__SMTP_USER: seu email
	- AIRFLOW__SMTP__SMTP_PASSWORD: senha gerada
	- AIRFLOW__SMTP__SMTP_PORT: 587
	- AIRFLOW__SMTP__MAIL_FROM: Airflow
