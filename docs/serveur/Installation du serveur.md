<link rel="stylesheet" type="text/css" href="../style/style.css">
<link rel="stylesheet" type="text/css" href="../style/dark-theme.css">
<link rel="stylesheet" type="text/css" href="../style/dark-code.css">

<!-- Side navigation -->
<div class="sidebar">
  <h1>Sommaire</h1>
  
  <a href="../Manuel%20du%20participant.html">Manuel du participant</a>
  <br/>
  <span>Serveur</span>
  <ul>
    <li><a href="Installation%20du%20serveur.html">Installation du serveur</a></li>
    <li><a href="Configuration%20du%20serveur.html">Configuration du serveur</a></li>
  </ul>
  <span>Technique</span>
  <ul>
    <li><a href="../tech/Contrats%20d'interfaces.html">Contrats d'interfaces</a></li>
    <li><a href="../tech/Contrats%20d'interfaces%20-%20Admin.html">Contrats d'interfaces - Admin</a></li>
  </ul>
</div>

<!-- Page content -->
<div class="main">

# Installation du serveur

- [Installation du serveur](#installation-du-serveur)
  - [Installation par scripts](#installation-par-scripts)
  - [Installation manuelle](#installation-manuelle)
    - [Prérequis](#prérequis)
    - [Environnement virtuel Python](#environnement-virtuel-python)
    - [Démarrer le serveur](#démarrer-le-serveur)


Vous devez avoir obtenu le fichier `battlebots-server-package.zip` au préalable. Ce fichier contient tout ce qu'il faut pour faire tourner le serveur Battlebots en local.

## Installation par scripts

> ⚠️ L'installation par script n'est actuellement disponible que pour **Windows**.

- Décompressez le fichier `battlebots-server-package.zip` dans un dossier de votre choix
- Lancer le fichier `install-server.bat` qui se trouve dans le dossier décompressé
- Lancer les serveurs Python et ActiveMQ via `start-server.bat` ou `start-server-debug.bat` suivant si vous voulez lancer en mode debug ou non (le mode debug est largement recommandé pour le développement)

Si tout fonctionne, vous devriez avoir 2 invites de commandes Windows de lancés :
- ActiveMQ démarré via Java
- Serveur python Battlebots

A partir de là vous devriez accéder à l'interface web via [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Installation manuelle

Cette méthode d'installation n'est pas recommandée. Elle est principalement présente pour expliquer sur quoi repose le serveur et pour aider si il doit être installé sur un OS différent.

### Prérequis

#### ActiveMQ 5.16.6

ActiveMQ sert les brokers de messages utilisés par le serveur pour envoyer des informations aux IA clientes. Les deux brokers de messages utilisés sont `STOMP` et `MQTT`.

ActiveMQ 5.16.6 est disponible ici (Windows et Linux) :
- [https://activemq.apache.org/components/classic/download/](https://activemq.apache.org/components/classic/download/)

C'est un zip à extraire dans le dossier de votre choix.

#### Java 1.8

Java 1.8 est nécessaire pour faire fonctionner les brokers de messages de ActiveMQ.  

Il peut être téléchargé ici en version installable (Windows, macOS et Linux) :
- [jre-8u361-linux-i586.rpm](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-i586.rpm)
- [jre-8u361-linux-i586.tar.gz](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-i586.tar.gz)
- [jre-8u361-linux-x64.rpm](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-x64.rpm)
- [jre-8u361-linux-x64.tar.gz](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-x64.tar.gz)
- [jre-8u361-macosx-x64.dmg](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-macosx-x64.dmg)
- [jre-8u361-solaris-sparcv9.tar.gz](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-solaris-sparcv9.tar.gz)
- [jre-8u361-windows-i586.exe](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-i586.exe)
- [jre-8u361-windows-x64.exe](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-x64.exe)

Ou en version portable (Windows uniquement) :
- [https://sourceforge.net/projects/portableapps/files/Java/](https://sourceforge.net/projects/portableapps/files/Java/)

#### Python 3.10

Il vous faut disposer d'une installation Python complète version **3.10** minimum (les versions "embeddable package" officielles ne sont **pas suffisantes**).

Il peut être téléchargé ici en version installable (Windows et macOS) :
- [https://www.python.org/downloads/release/python-31010/](https://www.python.org/downloads/release/python-31010/)

Ou en version portable (Windows uniquement) :
- [https://github.com/winpython/winpython/releases/tag/5.3.20221233](https://github.com/winpython/winpython/releases/tag/5.3.20221233) (la release `Winpython64-3.10.9.0dot` est suffisante)

### Environnement virtuel Python

- Décompressez le fichier `battlebots-server-package.zip` dans un dossier de votre choix
- Ouvrez un terminal dans ce dossier (le dossier doit contenir le fichier `main.py`) et créez un nouvel environnement virtuel :
  - Windows :
    - `<chemin vers votre binaire>\python.exe -m venv venv`
  - Unix :
    - `<chemin vers votre binaire>/python -m venv venv`
- Installer les libs nécessaires dans le venv créé :
  - Recopiez le dossier `site-packages` qui se trouve dans `third-party\python_venv_libs\` vers `venv\Lib\`

### Démarrer le serveur

#### ActiveMQ

On commence par démarrer le serveur ActiveMQ.

- Définir la variable `JAVA_HOME` sur votre installation de Java 1.8 :
  - Windows :
    - `set JAVA_HOME="<chemin absolu vers le dossier du JRE 1.8>"`
  - Unix :
    - `export JAVA_HOME=<chemin absolu vers le dossier du JRE 1.8>`
- Lancer le serveur :
  - Windows :
    - `third-party\activemq\bin\activemq.bat start`
  - Unix :
    - `third-party/activemq/bin/activemq start`

#### Python

Une fois ActiveMQ lancé, on peut démarrer le serveur Python.

- Windows :
  - `venv\Scripts\python.exe -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30`
- Unix :
  - `venv/Scripts/python -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30`

A partir de là vous devriez accéder à l'interface web via [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

[⬆️ Retour](#top) - _Installation du serveur_

</div>
