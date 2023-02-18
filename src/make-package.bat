@echo off
cls
chcp 65001 >nul
rem ---------------------------------

rem Suppression de l'ancienne version
del /Q battlebots-server-package.zip
del /Q battlebotslib.zip

rem Partie serveur
rem --------------
rem Création du dossier de serveur temporaire
set tmp_server=_tmp_server
rmdir /S /Q %tmp_server%
mkdir %tmp_server%

rem Recopie du code Python Serveur
robocopy /E server %tmp_server%

rem Suppression des dossiers inutiles
rmdir /S /Q %tmp_server%\.idea
rmdir /S /Q %tmp_server%\__pycache__
rmdir /S /Q %tmp_server%\activemq_config
del /Q %tmp_server%\activemq\data\*.log
rmdir /S /Q %tmp_server%\activemq\data\kahadb
rmdir /S /Q %tmp_server%\activemq\data\tmp
rmdir /S /Q %tmp_server%\venv
del /Q %tmp_server%\*.bak

rem Zip du package serveur
cd %tmp_server%
..\7za.exe a -tzip -r ..\battlebots-server-package *
cd ..

rem Suppression du dossier temporaire
rmdir /S /Q %tmp_server%


rem Partie lib client
rem -----------------
rem Création du dossier de package temporaire
set tmp_lib=_tmp_lib
rmdir /S /Q %tmp_lib%
mkdir %tmp_lib%
mkdir %tmp_lib%\battlebotslib

rem Recopie du code Python Serveur
robocopy /E battlebotslib %tmp_lib%\battlebotslib

rem Suppression des dossiers inutiles
rmdir /S /Q %tmp_lib%\battlebotslib\.idea

rem Zip du package serveur
cd %tmp_lib%
..\7za.exe a -tzip -r ..\battlebotslib *
cd ..

rem Suppression du dossier temporaire
rmdir /S /Q %tmp_lib%


pause
