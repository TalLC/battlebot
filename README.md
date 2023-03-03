![logo](https://github.com/TalLC/battlebot/raw/main/img/logo.png)

Plateforme de gestion de combat de robots virtuels.

---

# Documentation
- [Manuel du participant](src/docs/Manuel%20du%20participant.md)

## Messages
- [Contrats d'interfaces](src/docs/tech/Contrats%20d'interfaces.md)
- [Contrats d'interfaces - Admin](src/docs/tech/Contrats%20d'interfaces%20-%20Admin.md)

## Packaging
- [Packaging client et serveur](src/docs/packaging/Packaging%20client%20et%20serveur.md)

## Serveur
- [Installation du serveur](src/docs/serveur/Installation%20du%20serveur.md)
- [Configuration du serveur](src/docs/serveur/Configuration%20du%20serveur.md)
- [Interface du jeu](http://127.0.0.1:8000)
- [Web console ActiveMQ](https://127.0.0.1:8162/) : admin/admin
  - Pour les navigateurs basés sur Chromium, taper `thisisunsafe` sur votre clavier si la page est bloquée à cause du certificat auto signé
  
## Lib client
- [Installation de la lib](src/docs/client/Installation%20de%20la%20lib%20Python.md)
- [Utilisation de la classe BotAi](src/docs/tech/battlebotslib%20-%20BotAi.md)


# Client
## IA de test
### Pré-requis
Un script Python d'IA de test a été créée pour illustrer l'utilisation de la lib cliente.  
Un fichier `requirements.txt` est fourni et il faut avoir la lib client installée pour utiliser cette IA.
- [Code source](src/AI)

### Configuration
- [Config du bot](src/AI/bot1.json) (nom et id d'équipe)
- [Informations de connexions](src/AI/conf) (Rest, STOMP et MQTT)

