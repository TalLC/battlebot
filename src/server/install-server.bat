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

rem Création du dossier qui va recevoir les programmes à installer
mkdir third-party

echo.
echo.
echo ** CHECK DES PRÉREQUIS **

rem Vérification de la présence de Java 1.8
echo.
echo Vérification de la présence de Java 1.8...
rem check si java JRE est installé
reg query "HKLM\SOFTWARE\JavaSoft\Java Runtime Environment" >nul 2>&1
if %errorlevel% equ 0 (
    rem check si la version JRE 1.8 est installée
    reg query "HKLM\SOFTWARE\JavaSoft\Java Runtime Environment" | findstr /i "1.8" >nul 2>&1
    set "skip_java=true"
    if %errorlevel% equ 0 (
        rem JRE 1.8 est installé
        reg query "HKLM\SOFTWARE\JavaSoft\Java Runtime Environment" /v CurrentVersion | findstr /i "1.8" >nul 2>&1
        if %errorlevel% equ 0 (
            rem JRE 1.8 est installé et sélectionné
            echo → Java JRE 1.8 est installé.
        ) else (
            rem JRE 1.8 est installé mais non sélectionné
            echo → Java JRE 1.8 est installé mais n'est pas sélectionné :
            powershell write-host -fore Red Modifiez vos options Java pour cibler JRE 1.8 ou définissez la variable d`'environnement JAVA_HOME sur JRE 1.8
        )
    ) else (
        rem JRE 1.8 n'est pas installé
        echo → Java JRE 1.8 n'est pas installé.
        set "skip_java=false"
    )
) else (
    rem aucun JRE n'est installé
    echo → Java JRE n'est pas installé.
    set "skip_java=false"
)

rem Vérification de la présence de Python 3.10
echo.
echo Vérification de la présence de Python 3.10...
python -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo → Python 3.10 est déjà installé.
    set "skip_python=true"
) else (
    echo → Python 3.10 n'est pas installé.
    set "skip_python=false"
)

echo.
echo.
echo ** INSTALLATION DES PRÉREQUIS **

rem Téléchargement et installation de Java 1.8 x64
rem https://gist.github.com/wavezhang/ba8425f24a968ec9b2a8619d7c2d86a6
if not "%skip_java%"=="true" (
    echo Téléchargement et installation de Java 1.8 x64...
    cd third-party
    powershell.exe -Command "Invoke-WebRequest -Uri 'https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-x64.exe' -OutFile 'jre-8u361-windows-x64.exe'; Start-Process .\jre-8u361-windows-x64.exe -ArgumentList '/s' -Wait"
    cd ..
)

rem Téléchargement et installation de Python 3.10 x64
if not "%skip_python%"=="true" (
    echo Téléchargement et installation de Python 3.10 x64...
    cd third-party
    powershell.exe -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe' -OutFile 'python-3.10.10-amd64.exe'; Start-Process .\python-3.10.10-amd64.exe -ArgumentList '/quiet', 'InstallAllUsers=1', 'Include_test=0', 'PrependPath=1' -Wait"
    cd ..
)

echo.
echo.
echo ** CONFIGURATION DE L'ENVIRONNEMENT VIRTUEL PYTHON **

rem Récupération du Path de Python 3.10
for /f "tokens=2*" %%a in ('reg query "HKLM\SOFTWARE\Python\PythonCore\3.10\InstallPath" /v ExecutablePath ^| find /i "ExecutablePath"') do (
    set "python_path=%%b"
)
set "python_path=!python_path:"=!"

rem Création de l'environnement virtuel
echo Création de l'environnement virtuel...
"%python_path%" -m venv venv

rem Installation des packages PIP
rem On passe --use-pep517 pour la compatibilité avec la lib paho-mqtt
echo Installation des paquets pip...
venv\Scripts\pip.exe install --use-pep517 -r requirements.txt

:end
pause
