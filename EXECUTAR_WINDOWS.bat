@echo off
title API REST Segura - Gestao de Usuarios

if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Instalando dependencias...
python -m pip install -r requirements.txt

echo.
echo Iniciando aplicacao...
echo Interface: http://127.0.0.1:8000
echo Swagger:   http://127.0.0.1:8000/docs
echo.
python -m uvicorn app.main:app --reload

pause
