![logo](https://github.com/TalLC/battlebot/raw/main/img/logo.png)

Plateforme de gestion de combat de robots virtuels.

---

# Serveur

# Client
## IA de test

### Pré-requis
Un script Python d'IA de test a été créé pour illustrer l'utilisation de la lib cliente.  
Un fichier `requirements.txt` est fourni et il faut avoir la lib client installée pour utiliser cette IA.
- [Code source](src/AI)

### Configuration
On a plusieurs fichiers de config pour les connexions aux services Rest, STOMP et MQTT ainsi que pour les informations du bot (nom et équipe) :
- [Config du bot](src/AI/bot1.json)
- [Informations de connexions](src/AI/conf)

## Lib client Python
### Build la lib
- [Code source](src/battlebotslib-sources)
- [Comment build la lib](src/battlebotslib-sources/README.md)

### Utilisation de la lib Python
- [Doc d'utilisation de la lib](src/battlebotslib-sources/doc/BotAi%20library.md) ([PDF](src/battlebotslib-sources/doc/BotAi%20library.pdf))
- [Détail des messages reçus](src/battlebotslib-sources/doc/Messages.md) ([PDF](src/battlebotslib-sources/doc/Messages.pdf))

