![logo](https://github.com/TalLC/battlebot/raw/main/img/logo.png)

Plateforme de gestion de combat de robots virtuels.

---

# Serveur
## ActiveMQ
### Installation
- [Java JRE 1.8 (64 bits)](https://www.java.com/fr/download/manual.jsp) (pré-requis)

### Lancement
- Lancer le fichier [server/activemq/start.bat](src/server/activemq/start.bat)

### Console
- [Web console](https://127.0.0.1:8162/) : admin/admin
  - Pour les navigateurs basés sur Chromium, taper `thisisunsafe` sur votre clavier si la page est bloquée à cause du certificat auto signé

## Python
### Installation
- [Python 3.10 (64 bits)](https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe') (pré-requis)

Activer l'environnement virtuel du serveur, puis lancer la commande :
```
python.exe -m uvicorn main:app --port 8000 --reload --timeout-keep-alive 30
```


# Client
## IA de test
### Pré-requis
Un script Python d'IA de test a été créée pour illustrer l'utilisation de la lib cliente.  
Un fichier `requirements.txt` est fourni et il faut avoir la lib client installée pour utiliser cette IA.
- [Code source](src/AI)

### Configuration
- [Config du bot](src/AI/bot1.json) (nom et id d'équipe)
- [Informations de connexions](src/AI/conf) (Rest, STOMP et MQTT)

## Lib client Python
### Build la lib
- [Code source](src/battlebotslib-sources)
- [Comment build la lib](src/battlebotslib-sources/README.md)

### Utilisation de la lib Python
- [Doc d'utilisation de la lib](src/battlebotslib-sources/doc/BotAi%20library.md) ([PDF](src/battlebotslib-sources/doc/BotAi%20library.pdf))
- [Détail des messages reçus](src/battlebotslib-sources/doc/Messages.md) ([PDF](src/battlebotslib-sources/doc/Messages.pdf))

