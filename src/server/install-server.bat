@echo off
cls
chcp 65001 >nul
setlocal EnableDelayedExpansion
rem ---------------------------------
echo.
echo ______  _______ _______ _______        _______ ______   _____  _______ _______
echo ^|_____] ^|_____^|    ^|       ^|    ^|      ^|______ ^|_____] ^|     ^|    ^|    ^|______
echo ^|_____] ^|     ^|    ^|       ^|    ^|_____ ^|______ ^|_____] ^|_____^|    ^|    ______^|
echo.

rem Création du dossier qui va recevoir les programmes à installer
mkdir third-party

rem Vérification de la présence de Java 1.8
echo Vérification si Java 1.8 est déjà installé...
reg query "HKLM\SOFTWARE\JavaSoft\Java Runtime Environment" /v CurrentVersion >nul 2>&1
if %errorlevel% equ 0 (
    reg query "HKLM\SOFTWARE\JavaSoft\Java Runtime Environment" /v CurrentVersion | findstr /i "1.8" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Java 1.8 est déjà installé.
        set "skip_java=true"
    ) else (
        echo Java est installé, mais ce n'est pas la version 1.8. Veuillez définir votre variable d'environnement JAVA_HOME sur votre répertoire Java 1.8 et relancer l'installation.
        goto end
    )
) else (
    echo Java n'est pas installé.
    set "skip_java=false"
)

rem Vérification de la présence de Python 3.10
echo Vérification si Python 3.10 est déjà installé...
python -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo Python 3.10 est déjà installé.
    set "skip_python=true"
) else (
    echo Python 3.10 n'est pas installé.
    set "skip_python=false"
)

rem Télécharment et installation de Java 1.8 x64
if not "%skip_java%"=="true" (
    echo Télécharment et installation de Java 1.8 x64...
    cd third-party
    powershell.exe -Command "Invoke-WebRequest -Uri 'https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-x64.exe' -OutFile 'jre-8u361-windows-x64.exe'; Start-Process .\jre-8u361-windows-x64.exe -ArgumentList '/s' -Wait"
    cd ..
)

rem Télécharment et installation de Python 3.10 x64
if not "%skip_python%"=="true" (
    echo Télécharment et installation de Python 3.10 x64...
    cd third-party
    powershell.exe -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe' -OutFile 'python-3.10.10-amd64.exe'; Start-Process .\python-3.10.10-amd64.exe -ArgumentList '/quiet', 'InstallAllUsers=1', 'Include_test=0', 'PrependPath=1' -Wait"
    cd ..
)

rem Création de l'environnement virtuel
echo Création de l'environnement virtuel...
python -m venv venv

rem Installation des packages PIP
echo Installation des paquets pip...
venv\Scripts\pip.exe install -r requirements.txt

echo Installation terminée.

:end
pause