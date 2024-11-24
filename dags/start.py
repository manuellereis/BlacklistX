from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Defina os parâmetros de configuração para a DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 24),
    'retries': 1,
    'catchup': False,
}

# Criar a DAG
dag = DAG(
    'start_app_dag',
    default_args=default_args,
    description='DAG para rodar comandos de inicialização de aplicativo',
    schedule_interval=None,  # Define que a DAG será acionada manualmente
)

# Desativa o ambiente atual
deactivate_task = BashOperator(
    task_id='deactivate_env',
    bash_command="deactivate",
    dag=dag,
)

# Ativa o ambiente virtual
activate_task = BashOperator(
    task_id='activate_env',
    bash_command="source .venv/bin/activate",
    executable='/bin/bash',
    dag=dag,
)

# Inicia o comando 'takeout start'
takeout_task = BashOperator(
    task_id='takeout_start',
    bash_command="takeout start 1323fdc2ff55",
    dag=dag,
)

# Inicia o servidor Uvicorn
uvicorn_task = BashOperator(
    task_id='start_uvicorn',
    bash_command="uvicorn app:app --host 127.0.0.1 --port 8000 --reload",
    dag=dag,
)

# Inicia o script de reconhecimento facial
recognition_task = BashOperator(
    task_id='start_recognition',
    bash_command="python3 recognition.py",
    dag=dag,
)

# Definir a ordem de execução dos passos
deactivate_task >> activate_task >> takeout_task >> uvicorn_task >> recognition_task
