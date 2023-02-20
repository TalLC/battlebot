@echo off
cls
chcp 65001 >nul
setlocal EnableDelayedExpansion
rem ---------------------------------
echo.
echo 888888b.         d8888 88888888888 88888888888 888      8888888888 888888b.    .d88888b. 88888888888 .d8888b.  
echo 888  "88b       d88888     888         888     888      888        888  "88b  d88P" "Y88b    888    d88P  Y88b 
echo 888  .88P      d88P888     888         888     888      888        888  .88P  888     888    888    Y88b.      
echo 8888888K.     d88P 888     888         888     888      8888888    8888888K.  888     888    888     "Y888b.   
echo 888  "Y88b   d88P  888     888         888     888      888        888  "Y88b 888     888    888        "Y88b. 
echo 888    888  d88P   888     888         888     888      888        888    888 888     888    888          "888 
echo 888   d88P d8888888888     888         888     888      888        888   d88P Y88b. .d88P    888    Y88b  d88P 
echo 8888888P" d88P     888     888         888     88888888 8888888888 8888888P"   "Y88888P"     888     "Y8888P"  
echo.

set python_path=third-party\python3.10

echo.
echo.
echo ** CONFIGURATION DE L'ENVIRONNEMENT VIRTUEL PYTHON **

rem Création de l'environnement virtuel
echo Création de l'environnement virtuel...
%python_path%\python.exe -m venv venv

rem Installation des packages PIP
rem On passe --use-pep517 pour la compatibilité avec la lib paho-mqtt
echo Installation des paquets pip...
venv\Scripts\pip.exe install --use-pep517 -r requirements.txt

:end
pause
