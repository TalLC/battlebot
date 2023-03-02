# Installation du serveur

- [Installation du serveur](#installation-du-serveur)
  - [Installation par scripts](#installation-par-scripts)
  - [Installation manuelle](#installation-manuelle)
    - [Prérequis](#prérequis)
    - [Environnement virtuel Python](#environnement-virtuel-python)
    - [Démarrer le serveur](#démarrer-le-serveur)
  - [Configuration](#configuration)
    - [Nombre de joueurs en jeu](#nombre-de-joueurs-en-jeu)
    - [Carte de jeu](#carte-de-jeu)
    - [Mode debug](#mode-debug)
    - [Équipes](#équipes)
    - [Brokers et API Rest](#brokers-et-api-rest)
  - [Bots factices](#bots-factices)
    - [Ajouter des bots](#ajouter-des-bots)
    - [Contrôler un bot](#contrôler-un-bot)


Vous devez avoir obtenu le fichier `battlebots-server-package.zip` au préalable. Ce fichier contient tout ce qu'il faut pour faire tourner le serveur Battlebots en local.

## Installation par scripts

> ⚠️ L'installation par script n'est actuellement disponible que pour **Windows**.

- Décompressez le fichier `battlebots-server-package.zip` dans un dossier de votre choix
- Lancer le fichier `install-server.bat` qui se trouve dans le dossier décompressé
- Lancer les serveurs Python et ActiveMQ via `start-server.bat` ou `start-server-debug.bat` suivant si vous voulez lancer en mode debug ou non (le mode debug est largement recommandé pour le développement)

Si tout fonctionne, vous devriez avoir 2 invites de commandes Windows de lancés :
- ActiveMQ démarré via Java
- Serveur python Battlebots

A partir de là vous devriez accéder à l'interface web via http://127.0.0.1:8000.


## Installation manuelle

Cette méthode d'installation n'est pas recommandée. Elle est principalement présente pour expliquer sur quoi repose le serveur et pour aider si il doit être installé sur un OS différent.

### Prérequis

#### ActiveMQ 5.16.6

ActiveMQ sert les brokers de messages utilisés par le serveur pour envoyer des informations aux IA clientes. Les deux brokers de messages utilisés sont `STOMP` et `MQTT`.

ActiveMQ 5.16.6 est disponible ici (Windows et Linux) :
- https://activemq.apache.org/components/classic/download/

C'est un zip à extraire dans le dossier de votre choix.

#### Java 1.8

Java 1.8 est nécessaire pour faire fonctionner les brokers de messages de ActiveMQ.  

Il peut être téléchargé ici en version installable (Windows, macOS et Linux) :
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-i586.rpm
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-i586.tar.gz
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-x64.rpm
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-linux-x64.tar.gz
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-macosx-x64.dmg
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-solaris-sparcv9.tar.gz
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-i586.exe
- https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jre/jre-8u361-windows-x64.exe

Ou en version portable (Windows uniquement) :
- https://sourceforge.net/projects/portableapps/files/Java/

#### Python 3.10

Il vous faut disposer d'une installation Python complète version **3.10** minimum (les versions "embeddable package" officielles ne sont **pas suffisantes**).

Il peut être téléchargé ici en version installable (Windows et macOS) :
- https://www.python.org/downloads/release/python-31010/ 

Ou en version portable (Windows uniquement) :
- https://github.com/winpython/winpython/releases/tag/5.3.20221233 (la release `Winpython64-3.10.9.0dot` est suffisante)

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

A partir de là vous devriez accéder à l'interface web via http://127.0.0.1:8000.

## Configuration

### Nombre de joueurs en jeu

Le définition du nombre de joueurs se fait via le fichier `conf\game.json` et le champs `max_players`.

Actuellement, le nombre maximum de joueurs est également le nombre de joueurs requis pour démarrer la partie.


### Carte de jeu

Le choix de la carte se fait via le fichier `conf\game.json` et le champs `map_id` (nom du fichier map).

Pour être prise en compte, la carte doit être présente dans le dossier `data\maps\`.


### Mode debug

En passant par les scripts de lancement, le mode debug set automatiquement.

Pour l'activer/désactiver manuellement, il faut modifier le fichier `conf\game.json` et passer la valeur de `is_debug` à `true` ou `false.`


### Équipes

Les équipes sont déclarées dans le fichier `conf\teams.json`. L'ID d'une équipe peut être défini dans ce fichier, sinon il sera généré automatiquement au lancement du serveur.

Vous les retrouverez tous dans la console au lancement du serveur, sous cette forme :
```
[INFO] 02/03/2023 05:41:23 - [MAIN] Created teams:
[INFO] 02/03/2023 05:41:23 - Blue team (team-id-1) - COLOR: 0x0042aa, BOTS: 0/1
[INFO] 02/03/2023 05:41:23 - Red team (team-id-2) - COLOR: 0xaa0000, BOTS: 0/1
[INFO] 02/03/2023 05:41:23 - Green team (team-id-3) - COLOR: 0x00bb00, BOTS: 0/1
[INFO] 02/03/2023 05:41:23 - Yellow team (f7e09fcc-73dc-466e-9ce6-3da97aaf5c15) - COLOR: 0xffcc00, BOTS: 0/1
[INFO] 02/03/2023 05:41:23 - Black team (f873a159-518b-4db5-8598-5e859435e07a) - COLOR: 0x101010, BOTS: 0/1
[INFO] 02/03/2023 05:41:23 - White team (d6214344-e3d3-4b6f-925a-6e51936d8150) - COLOR: 0xdadada, BOTS: 0/1
```


### Brokers et API Rest

Les informations de connexion aux brokers et le mot de passe admin de l'API Rest (par défaut : `password`) sont disponibles respectivement dans les fichiers :
- `rest.json`
- `mqtt.conf`
- `stomp.conf`


## Bots factices

Des bots sans IA peuvent être ajoutés à votre partie. Ils permettent de remplir le nombre de joueurs requis sans avoir à connecter plusieurs IA.

Le mode debug du serveur est indispensable pour ajouter et contrôler des bots factices.

Ils peuvent également être contrôlés manuellement depuis l'interface Web, ce qui est pratique pour tirer sur sa propre IA et déclencher les messages de dégâts.

### Ajouter des bots

Démarrez le serveur en mode debug et lancez l'interface du jeu (http://127.0.0.1:8000).

Sur la page d'attente de Battlebots, vous remarquerez un bouton `Connecter un bot 🤖` en bas à droite. Ce bouton permet d'ajouter un bot sans IA à la partie. Il prendra la première équipe disponible sans joueurs.

### Contrôler un bot

Double cliquez sur un bot à l'écran, une télécommande va s'afficher sur la droite de l'écran pour prendre le contrôle du bot.

