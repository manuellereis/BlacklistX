[GERENTIATOR LIBS]
UV 
    -> UV INIT
    -> UV VENV
    -> UV ADD
    -> UV PIP INSTALL

uvicorn app:app --host 127.0.0.1 --port 8000 --reload

pip install apache-airflow --no-deps