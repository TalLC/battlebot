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

set third_party=third-party
set python_path=%third_party%\python3.10

echo.
echo.
echo ** CONFIGURATION DE L'ENVIRONNEMENT VIRTUEL PYTHON **

rem Création de l'environnement virtuel
echo Création de l'environnement virtuel...
%python_path%\python.exe -m venv venv

rem Recopie des packages PIP
echo Recopie des paquets pip...
cd %third_party%
robocopy /E python_venv_libs ..\venv\Lib\ > nul

pause
