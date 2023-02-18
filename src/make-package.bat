@echo off
cls
chcp 65001 >nul
rem ---------------------------------

rem Suppression de l'ancienne version
del /Q battlebots-server-package.zip

rem Création du dossier de package serveur final
rmdir /S /Q _package
mkdir _package

rem Recopie du code Python Serveur
robocopy /E server _package

rem Suppression des dossiers inutiles
rmdir /S /Q _package\.idea
rmdir /S /Q _package\__pycache__
rmdir /S /Q _package\activemq_config
del /Q _package\activemq\data\*.log
rmdir /S /Q _package\activemq\data\kahadb
rmdir /S /Q _package\activemq\data\tmp
rmdir /S /Q _package\venv
del /Q _package\*.bak

rem Zip du package serveur
cd _package
..\7za.exe a -tzip -r ..\battlebots-server-package *
cd ..

rem Zip du package de la lib client
cd battlebotslib-sources
..\7za.exe a -tzip -r ..\battlebots-client-lib *
cd ..

pause