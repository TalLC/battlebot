# Besoins

## Général
- Durée d'une partie :
  - Choix du temps : illimité à X minutes
  - Compétition : 5 à 10 minutes

- Nombre de joueurs :
  - 1 à X

- Modes de jeux :
  - Free-4-all (10 Joueurs)
  - Par équipe (1 VS 1, 5 VS 5)

- Conditions de victoire :
  - Par ordre d'élimination

- Connexion à une partie :
  - Nom d'arène
  - Token du robot
  - possible d'autoriser les robots pouvant se connecter à l'arène (whitelist)


- Administrateur :
  - Donner les droits d'accès priviligier (BDD) pour administrer un tournois
  - Appels REST pour modifier la BDD (changer nom de robot, ajouter un token)

- Mode entrainement :
  - Arènes prédéfinies avec des IA dedans
  - Au moins 1 arène avec 1 équipe robot dedans
  - Se base sur le nom de l'arêne (= nom réservé)


## Arènes
- Timer pré-défini
- Mode de jeu
- Des équipes (whitelistées)


### Pickups
- Munitions
- Boucliers
- Boost de vitesse


## Equipe
- Nom
- Des robots (1 à X)


## Robot
- Nom
- 100 PV
- Vitesse
- Coordonnées
- Heading
- Champs de vision
- 1 Arme
- 1 Bouclier


### Arme
- Dégâts
- Portée
- Largeur
- Temps de recharge
- Munitions


### Bouclier
- 150 PV
- % d'absorbtion
- Bloque les mouvements
- Peut casser


## Réflexion
- respawn => Non
- armes différentes => 2 armes inclues
- heal (dégats négatif) => Non
- Faire une IA évolutive
- 3D : PNG skin robot
- Logo : PNG logo
- Arène : Skin Urbain, Forêt, Glace, ...


## Commandes (Synchrone/REST)

### Générales
- Avancer (jusqu'à arrêt)
- S'arrêter
- Tourner (Droite, Gauche à +/- 10°)
- Tourner (définir l'angle final)
- Tirer
- Protéger


### GPS
- Bloque le robot
- Renvoie coordonnées
- Renvoie heading



## Récupération permanente (MQTT)
- Informations générales concernant le robot
- Durée de vie max des messages pour éviter que le joueur ne récupère des messages obsolètes

### Radar de vision
- Champs de vision du Robot
- Envoie tout ce qui est détecté dans un tableau d'objets
- Objet :
  - Angle
  - Distance
  - Type détecté (pickup, ennemie, mur)

### Evenementiel
- Evenements :
  - Collision
  - Tiré dessus
  - Pickup ramassé

## Récupération ponctuelle
- Informations requêtées (on regarde les jauges)
- 1 événement = 1 donnée renvoyée dans la file de type :
  - "pv = x"
  - "shield = x"
- Le joueur doit requêter les éléments 1 à 1


------

| id_equipe | nom_equipe | liste_ID_Robot
|----|----|----| 
| 1 | Equipe bleu | [] |
| 2 | Equipe rouge | [2,1] |


| id_robot | id_equipe | token | nom_robot |
|----|----|----|----|
| 1 | 2 | AEQSFSF | ROBOBO
| 2 | 2 | FSFAEQS | ROBOBO


| nom_arene | timer | whitelist_teams | mode |
|----|----|----|----|
| blabla | 05:00 | [Equipe_bleu, Equipe_rouge] | FFA |

