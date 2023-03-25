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

# Configuration du serveur

- [Configuration du serveur](#configuration-du-serveur)
  - [Nombre de joueurs en jeu](#nombre-de-joueurs-en-jeu)
  - [Carte de jeu](#carte-de-jeu)
  - [Mode debug](#mode-debug)
  - [Équipes](#équipes)
  - [Brokers et API Rest](#brokers-et-api-rest)
  - [Bots factices](#bots-factices)
    - [Ajouter des bots](#ajouter-des-bots)
    - [Contrôler un bot](#contrôler-un-bot)
  - [Troubleshooting](#troubleshooting)
    - [La console web ActiveMQ est bloquée pour problème de certificat](#la-console-web-activemq-est-bloquée-pour-problème-de-certificat)
    - [Erreur ActiveMQ : User user is not authorized to create...](#erreur-activemq--user-user-is-not-authorized-to-create)


## Nombre de joueurs en jeu

Le définition du nombre de joueurs se fait via le fichier `conf\game.json` et le champs `max_players`.

Actuellement, le nombre maximum de joueurs est également le nombre de joueurs requis pour démarrer la partie.


## Carte de jeu

Le choix de la carte se fait via le fichier `conf\game.json` et le champs `map_id` (nom du fichier map).

Pour être prise en compte, la carte doit être présente dans le dossier `data\maps\`.


## Mode debug

En passant par les scripts de lancement, le mode debug set automatiquement.

Pour l'activer/désactiver manuellement, il faut modifier le fichier `conf\game.json` et passer la valeur de `is_debug` à `true` ou `false.`


## Équipes

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


## Brokers et API Rest

Les informations de connexion aux brokers et le mot de passe admin de l'API Rest (par défaut : `password`) sont disponibles respectivement dans les fichiers :
- `rest.json`
- `mqtt.conf`
- `stomp.conf`


## Bots factices

Des bots sans IA peuvent être ajoutés à votre partie. Ils permettent de remplir le nombre de joueurs requis sans avoir à connecter plusieurs IA.

Le mode debug du serveur est indispensable pour ajouter et contrôler des bots factices.

Ils peuvent également être contrôlés manuellement depuis l'interface Web, ce qui est pratique pour tirer sur sa propre IA et déclencher les messages de dégâts.

### Ajouter des bots

Démarrez le serveur en mode debug et lancez l'interface du jeu ([http://127.0.0.1:8000](http://127.0.0.1:8000)).

Sur la page d'attente de Battlebots, vous remarquerez un bouton `Connecter un bot` en bas à droite. Ce bouton permet d'ajouter un bot sans IA à la partie :

<img src="../img/debug-add-bot.png"> 

Il prendra la première équipe disponible sans joueurs.

Si vous n'avez pas ce bouton, c'est que le serveur n'est pas lancé en mode debug.

### Contrôler un bot

Double cliquez sur un bot à l'écran, une télécommande va s'afficher sur la droite de l'écran pour prendre le contrôle du bot.

## Troubleshooting

### La console web ActiveMQ est bloquée pour problème de certificat

C'est souvent dû à l'utilisation d'un certificat auto signé pour héberger le site. Sous Firefox on peut continuer malgré le message mais pour les navigateurs basés sur Chromium, il faut taper `thisisunsafe` sur votre clavier pour passer à la suite.

### Erreur ActiveMQ : User user is not authorized to create...

Vérifiez vos informations de connexion aux services STOMP et MQTT, il peut s'agir d'une mauvaise notation du nom de file à écouter (inversion entre les `.` utilisés par STOMP et les `/` utilisés par MQTT).

---

[⬆️ Retour](#top) - _Configuration du serveur_

</div>
