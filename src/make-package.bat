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
set third_party=server\third-party
rem Python
set python_package=Winpython64-3.10.9.0dot
set python_package_dir=WPy64-31090\python-3.10.9.amd64
set python_final_dir=python3.10
rem Java
set java_package=jre-8u361-windows-x64
set java_package_dir=jre1.8.0_361
set java_final_dir=jre1.8.0
rem ActiveMQ
set amq_package=apache-activemq-5.16.6-bin
set amq_package_dir=apache-activemq-5.16.6
set amq_final_dir=activemq
set amq_config_dir=activemq_config


rmdir /S /Q %tmp_server%
mkdir %third_party%

rem Téléchargement de Java JRE 1.8
echo Check de la présence de Java...
if not exist %third_party%\%java_final_dir%\ (
    echo Téléchargement de Java...
    powershell.exe -Command "$ProgressPreference = 'SilentlyContinue';Invoke-WebRequest -UserAgent 'Wget' -Uri 'https://sourceforge.net/projects/portableapps/files/Java/%java_package%.tar.gz/download' -OutFile '%third_party%\%java_package%.tar.gz';"
    cd %third_party%
    ..\..\7za.exe x "%java_package%.tar.gz" -o* -y > nul
    ..\..\7za.exe x "%java_package%.tar" -o* -y > nul
    move "%java_package%\%java_package_dir%" "%java_final_dir%"
    ping 127.0.0.1 -n 2 > nul
    rmdir /S /Q "%java_package%.tar"
    ping 127.0.0.1 -n 2 > nul
    rmdir /S /Q "%java_package%"
    del /Q "%java_package%.tar.gz"
    cd ..\..
)

rem Téléchargement de Python
echo Check de la présence de Python...
if not exist %third_party%\%python_final_dir%\ (
    echo Téléchargement de Python...
    powershell.exe -Command "$ProgressPreference = 'SilentlyContinue';Invoke-WebRequest -Uri 'https://github.com/winpython/winpython/releases/download/5.3.20221233/%python_package%.exe' -OutFile '%third_party%\%python_package%.exe';
    cd %third_party%
    "%python_package%.exe" -o* -y
    ping 127.0.0.1 -n 2 > nul
    move "%python_package%\%python_package_dir%" "%python_final_dir%"
    ping 127.0.0.1 -n 2 > nul
    rmdir /S /Q "%python_package%"
    del /Q "%python_package%.exe"
    cd ..\..
)

rem Téléchargement de ActiveMQ
echo Check de la présence de ActiveMQ...
if not exist %third_party%\%amq_final_dir%\ (
    echo Téléchargement de ActiveMQ...
    powershell.exe -Command "$ProgressPreference = 'SilentlyContinue';Invoke-WebRequest -Uri 'https://www.apache.org/dyn/closer.cgi?filename=/activemq/5.16.6/%amq_package%.zip&action=download' -OutFile '%third_party%\%amq_package%.zip';
    cd %third_party%
    ..\..\7za.exe x "%amq_package%.zip" -o* -y  > nul
    ping 127.0.0.1 -n 2 > nul
    move "%amq_package%\%amq_package_dir%" "%amq_final_dir%"
    ping 127.0.0.1 -n 2 > nul
    rmdir /S /Q "%amq_package%"
    del /Q "%amq_package%.zip"
    cd ..\..
)

rem Configuration de ActiveMQ
cd %third_party%
robocopy %amq_config_dir% %amq_final_dir%  > nul
cd ..\..

rem Recopie du code Python Serveur
mkdir %tmp_server%
robocopy /E server %tmp_server%  > nul

rem Suppression des dossiers inutiles
rmdir /S /Q %tmp_server%\.idea
rmdir /S /Q %tmp_server%\__pycache__
rmdir /S /Q %tmp_server%\activemq
rmdir /S /Q %tmp_server%\activemq_config
del /Q %tmp_server%\activemq\data\*.log
rmdir /S /Q %tmp_server%\activemq\data\kahadb
rmdir /S /Q %tmp_server%\activemq\data\tmp
rmdir /S /Q %tmp_server%\venv
del /Q %tmp_server%\*.bak

rem Zip du package serveur
cd %tmp_server%
..\7za.exe a -tzip -r ..\battlebots-server-package *  > nul
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
robocopy /E battlebotslib %tmp_lib%\battlebotslib  > nul

rem Suppression des dossiers inutiles
rmdir /S /Q %tmp_lib%\battlebotslib\.idea

rem Zip du package serveur
cd %tmp_lib%
..\7za.exe a -tzip -r ..\battlebotslib *
cd ..

rem Suppression du dossier temporaire
rmdir /S /Q %tmp_lib%


pause
