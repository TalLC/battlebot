# Packaging client et serveur

- [Packaging client et serveur](#packaging-client-et-serveur)
  - [Build de la lib client](#build-de-la-lib-client)
    - [Prérequis au build du package](#prérequis-au-build-du-package)
    - [Build la lib](#build-la-lib)
    - [Installation de la lib](#installation-de-la-lib)
  - [Packaging](#packaging)
    - [Dossier serveur third-party](#dossier-serveur-third-party)
    - [Créer les packages](#créer-les-packages)


## Build de la lib client

Le package client se trouve dans `battlebot\src\battlebotslib`. Les sources sont dans le sous-dossier `battlebotslib` (c'est ce code qui est appelé quand on importe le package dans Python).  
La classe principale que les joueurs vont utiliser est `BotAi` :
```py
from battlebotslib.BotAi import BotAi
```

Quand on fait une modification dans le code du paquet, il faut le rebuild pour pouvoir le réinstaller via PIP.

### Prérequis au build du package

- Créer votre venv dans ce dossier (`battlebot\src\battlebotslib`) :
  - `python3 -m venv venv`
- Activer l'environnement :
  - `venv\Scripts\activate.bat`
- Installer les prérequis au build
  - `pip install wheel setuptools twine`

### Build la lib

- Toujours dans le dossier `battlebot\src\battlebotslib`, build la lib :
  - `python setup.py bdist_wheel`

Un fichier `.whl` est créé dans le dossier `dist`, c'est lui que l'on va passer en paramètre de PIP pour installer le package.

### Installation de la lib
- Se placer dans son dossier de projet IA
- Créer un `venv` si ce n'est pas déjà fait
- Installer le paquet via PIP :
  - `pip install dist\battlebotslib-0.4.0-py3-none-any.whl`

En cas de modification du code de la lib, il faudra désinstaller le package avant de le réinstaller :
- `pip uninstall dist\battlebotslib-0.4.0-py3-none-any.whl`

## Packaging

### Dossier serveur third-party

Le dossier `battlebot\src\server\third-party` existe pour contenir les application tierces et fichiers de configuration. On y retrouve notamment :
- (*) Java JRE 8u361
- (*) Python portable 3.10
- (*) ActiveMQ 5.16.6
- Configuration pour ActiveMQ
- Libs pour le venv serveur Python
  
_(*) non présent sur Git car téléchargés lors de la création du package_

### Créer les packages

Lancer le script `battlebot\src\make-package.bat` et le laisser dérouler.  
Ce script s'occupe de :
- Packager la partie serveur :
  - Télécharger Java JRE 8u361 dans `third-party\jre1.8.0` si le dossier n'existe pas déjà
  - Télécharger Python 3.10 dans `third-party\python3.10` si le dossier n'existe pas déjà
  - Télécharger ActiveMQ 5.16.6 dans `third-party\activemq` si le dossier n'existe pas déjà
  - Recopier les fichiers de configuration de `third-party\activemq_config` dans `third-party\activemq`
  - Recopier tout le dossier `battlebot\src\server\` dans un répertoire temporaire
  - Le nettoyer des fichiers dont on veut se débarasser (`.idea`, `__pycache__`, `venv`, ...)
  - Zipper le dossier temporaire dans un fichier `battlebots-server-package.zip`
- Packager la lib client
  - Recopier tout le dossier `battlebot\src\battlebotslib\` dans un répertoire temporaire
  - Le nettoyer des fichiers dont on veut se débarasser (`.idea`, `venv`, ...)
  - Zipper le dossier temporaire dans un fichier `battlebotslib.zip`

Les fichiers zip générés sont prêt à être transmis aux joueurs.
