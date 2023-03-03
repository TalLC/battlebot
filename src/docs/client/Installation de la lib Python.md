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
    <li><a href="../serveur/Installation%20du%20serveur.html">Installation du serveur</a></li>
    <li><a href="../serveur/Configuration%20du%20serveur.html">Configuration du serveur</a></li>
  </ul>
  <span>Client</span>
  <ul>
    <li><a href="../client/Installation%20de%20la%20lib%20Python.html">Installation de la lib Python</a></li>
  </ul>
  <span>Technique</span>
  <ul>
    <li><a href="../tech/battlebotslib%20-%20BotAi.html">battlebotslib - BotAi</a></li>
    <li><a href="../tech/Contrats%20d'interfaces.html">Contrats d'interfaces</a></li>
    <li><a href="../tech/Contrats%20d'interfaces%20-%20Admin.html">Contrats d'interfaces - Admin</a></li>
  </ul>
</div>

<!-- Page content -->
<div class="main">

<center><img src="../img/Python-logo-notext.svg"></center>

# Installation de la lib Python

Vous devez avoir obtenu le fichier `battlebotslib.zip` au préalable. Ce fichier contient la bibliothèque Python à installer via PIP dans votre projet d'IA.

## Installation

Il est recommandé de vous créer un environnement virtuel au sein de votre projet et de l'activer avant d'installer la bibliothèque et ses dépendances.

Pour créer un environnement virtuel Python :
- `python -m venv venv`

Activer l'environnement virtuel :
- Windows :
  - `venv\Scripts\activate.bat`
- Unix :
  - `source venv/Scripts/activate`

Installer la lib :
- `pip install dist\battlebotslib-0.4.0-py3-none-any.whl`


Après l'installation, vous êtes prêt à utiliser la bibliothèque.

La classe principale permettant d'interagir avec votre IA est `battlebotslib.BotAi`.

---

[⬆️ Retour](#top) - _Installation de la lib Python_

</div>
