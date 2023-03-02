@echo off
cls
chcp 65001 >nul
rem ---------------------------------
rem Suppression du mode debug
del /Q conf\debug.dat 2> nul

rem utilisation du Java portable
set JAVA_HOME="%cd%\third-party\jre1.8.0"

rem Lancement de ActiveMQ
echo Lancement des brokers ActiveMQ
start cmd /C %cd%\third-party\activemq\bin\activemq.bat start

rem Attente de 10 secondes
echo Laisser le temps à ActiveMQ de démarrer (quelques secondes)
ping 127.0.0.1 -n 10 > nul

rem Lancement du serveur Battlebots
echo Lancement du serveur
venv\Scripts\python.exe -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30
