<link rel="stylesheet" type="text/css" href="../style/style.css">

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
  - [Installation par Docker](#installation-par-docker)
    - [Chargement du fichier image](#chargement-du-fichier-image)
    - [Démarrage d'un conteneur en ligne de commande](#démarrage-dun-conteneur-en-ligne-de-commande)
    - [Démarrage d'un conteneur avec docker compose](#démarrage-dun-conteneur-avec-docker-compose)
    - [Debug](#debug)
  - [Installation par scripts](#installation-par-scripts)
  - [Installation manuelle](#installation-manuelle)
    - [Prérequis](#prérequis)
    - [Environnement virtuel Python](#environnement-virtuel-python)
    - [Démarrer le serveur](#démarrer-le-serveur)


## Installation par Docker

Vous devez disposer d'une installation Docker permettant de lancer des conteneurs Linux au préalable.

### Chargement du fichier image

Importez l'image Docker à partir du fichier tar en utilisant la commande `docker load` :

```sh
docker load -i battlebots-0.5.2.tar
```

### Démarrage d'un conteneur en ligne de commande

Pour démarrer un conteneur à partir de l'image Docker, utilisez la commande `docker run` :

```sh
docker run -d --rm -p 8000:8000 -p 61613:61613 -p 1883:1883 battlebots:0.5.2
```

Explication des options utilisées :
- -d : Détache le conteneur et le fait s'exécuter en arrière-plan.
- -p 8000:8000 : (serveur web + REST) Mappe le port local 8000 sur le port 8000 du conteneur.
- -p 61613:61613 : (serveur STOMP) Mappe le port local 61613 sur le port 61613 du conteneur.
- -p 1883:1883 : (serveur MQTT) Mappe le port local 1883 sur le port 1883 du conteneur.
- battlebots:0.5.2 : Spécifie le nom et le tag de l'image à utiliser pour démarrer le conteneur.


### Démarrage d'un conteneur avec docker compose

Si vous avez Docker compose et souhaitez l'utiliser :

- Créez un fichier nommé `docker-compose.yml` dans un répertoire de votre choix :

```yml
version: '3'
services:
  battlebots:
    image: battlebots:0.5.2
    ports:
      - 8000:8000
      - 61613:61613
      - 1883:1883
    environment:
      - BATTLEBOTS_DEBUG=false
```

- Placez-vous dans le répertoire où se trouve le fichier `docker-compose.yml`
- Exécutez la commande suivante pour démarrer le conteneur en utilisant Docker Compose :

```sh
docker-compose up -d
```

Explication des options utilisées :
- -d : Détache le conteneur et le fait s'exécuter en arrière-plan.



### Debug

Pour activer le mode débug, passer la variable d'environnement `BATTLEBOTS_DEBUG` à `true`.

En ligne de commande :

```sh
docker run -d --rm -p 8000:8000 -p 61613:61613 -p 1883:1883 -e BATTLEBOTS_DEBUG=true battlebots:0.5.2
```

Dans le fichier `docker-compose.yml`
```yml
    ...
    environment:
      - BATTLEBOTS_DEBUG=true
```


## Installation par scripts

Vous devez avoir obtenu le fichier `battlebots-server-package.zip` au préalable. Ce fichier contient tout ce qu'il faut pour faire tourner le serveur Battlebots en local.

> ⚠️ L'installation par script n'est actuellement disponible que pour **Windows**.

- Décompressez le fichier `battlebots-server-package.zip` dans un dossier de votre choix
- Lancer le fichier `install-server.bat` qui se trouve dans le dossier décompressé
- Lancer les serveurs Python et ActiveMQ via `start-server.bat` ou `start-server-debug.bat` suivant si vous voulez lancer en mode debug ou non (le mode debug est largement recommandé pour le développement)

Si tout fonctionne, vous devriez avoir 2 invites de commandes Windows de lancés :
- ActiveMQ démarré via Java
- Serveur python Battlebots

A partir de là vous devriez accéder à l'interface web via [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Installation manuelle

Vous devez avoir obtenu le fichier `battlebots-server-package.zip` au préalable. Ce fichier contient tout ce qu'il faut pour faire tourner le serveur Battlebots en local.

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
- Windows [jre-8u361-windows-x64.exe](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-x64.exe)
- Linux [jre-8u361-linux-x64.rpm](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-x64.rpm)
- MacOs [jre-8u361-macosx-x64.dmg](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-macosx-x64.dmg)

Ou en version portable :
- Windows [jre-8u371-windows-x64.tar.gz](https://sourceforge.net/projects/portableapps/files/Java/)
- Linux  [jre-8u361-linux-x64.tar.gz](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-x64.tar.gz)

#### Python 3.10

Il vous faut disposer d'une installation Python complète version **3.10** minimum (les versions "embeddable package" officielles ne sont **pas suffisantes**).

Il peut être téléchargé ici en version installable (Windows et macOS) :
- Multi-plateformes [https://www.python.org/downloads/release/python-31010/](https://www.python.org/downloads/release/python-31010/)

Ou en version portable :
- Windows [https://github.com/winpython/winpython/releases/tag/5.3.20221233](https://github.com/winpython/winpython/releases/tag/5.3.20221233) (la release `Winpython64-3.10.9.0dot` est suffisante)
- MacOs [https://github.com/indygreg/python-build-standalone/releases/tag/20230507](https://github.com/indygreg/python-build-standalone/releases/tag/20230507) (release `cpython-3.10.11+20230507-<architecture>-unknown-linux-gnu-install_only.tar.gz`)
- Linux [https://github.com/indygreg/python-build-standalone/releases/tag/20230507](https://github.com/indygreg/python-build-standalone/releases/tag/20230507) (release `cpython-3.10.11+20230507-<architecture>-apple-darwin-install_only.tar.gz`)

### Environnement virtuel Python

- Décompressez le fichier `battlebots-server-package.zip` dans un dossier de votre choix
- Ouvrez un terminal dans ce dossier (le dossier doit contenir le fichier `main.py`) et créez un nouvel environnement virtuel :
  - Windows :
    - `<chemin vers votre binaire>\python.exe -m venv venv`
  - Linux :
    - `<chemin vers votre binaire>/python -m venv venv`
- Installer les libs nécessaires dans le venv créé :
  - Windows :
    - `venv\Scripts\pip install -r requirements.txt`
  - Linux :
    - `venv/bin/pip install -r requirements.txt`

### Démarrer le serveur

#### ActiveMQ

On commence par démarrer le serveur ActiveMQ.
Toujours dans le dossier principal de Battlebots, ouvrez un nouveau terminal.

- Définir la variable `JAVA_HOME` sur votre installation de Java 1.8 :
  - Windows :
    - `set JAVA_HOME="<chemin absolu vers le dossier du JRE 1.8>"`
  - Linux :
    - `export JAVA_HOME=<chemin absolu vers le dossier du JRE 1.8>`
- Lancer le serveur :
  - Windows :
    - `third-party\activemq\bin\activemq.bat start`
  - Linux :
    - `third-party/activemq/bin/activemq start` (ajoutez le droit d'exécution sur le fichier si nécessaire)

#### Python

Une fois ActiveMQ lancé, on peut démarrer le serveur Python.

- Windows :
  - `venv\Scripts\python.exe -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30`
- Unix :
  - `venv/bin/python -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30`

A partir de là vous devriez accéder à l'interface web via [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

[⬆️ Retour](#top) - _Installation du serveur_

</div>
