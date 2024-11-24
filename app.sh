#!/bin/bash

# Ativa o ambiente virtual
if [ -d ".venv" ]; then
    . .venv/bin/activate
    echo "Ambiente virtual ativado com sucesso."

    # Inicia o serviço Takeout
    takeout start 1323fdc2ff55 &
    echo "Takeout iniciado."

    # Inicia o servidor Uvicorn em segundo plano
    uvicorn scripts.web:app --host 127.0.0.1 --port 8000 --reload &
    echo "Servidor Uvicorn iniciado."

    # Executa o script de reconhecimento facial
    python3 scripts/recognition.py &
    echo "Script de reconhecimento facial iniciado."

    # Aguarda que os processos em segundo plano sejam encerrados
    wait
else
    echo "Erro: O ambiente virtual '.venv' não foi encontrado."
    exit 1
fi
