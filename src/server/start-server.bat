@echo off
cls
chcp 65001 >nul
rem ---------------------------------
echo Lancement des brokers ActiveMQ
start cmd /k activemq\bin\activemq.bat start

echo Laisser le temps à ActiveMQ de démarrer (quelques secondes)
timeout /t 10

echo Lancement du serveur
venv\Scripts\python.exe -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30
