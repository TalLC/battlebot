@echo off
echo Lancement du serveur
.\venv\Scripts\python.exe -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30