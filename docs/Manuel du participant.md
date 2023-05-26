<link rel="stylesheet" type="text/css" href="style/style.css">

<!-- Side navigation -->
<div class="sidebar">
  <h1>Sommaire</h1>
  
  <a href="Manuel%20du%20participant.html">Manuel du participant</a>
  <br/>
  <span>Serveur</span>
  <ul>
    <li><a href="serveur/Installation%20du%20serveur.html">Installation du serveur</a></li>
    <li><a href="serveur/Configuration%20du%20serveur.html">Configuration du serveur</a></li>
  </ul>
  <span>Technique</span>
  <ul>
    <li><a href="tech/Contrats%20d'interfaces.html">Contrats d'interfaces</a></li>
    <li><a href="tech/Contrats%20d'interfaces%20-%20Admin.html">Contrats d'interfaces - Admin</a></li>
  </ul>
</div>

<!-- Page content -->
<div class="main">

<center><img src="img/logo.png" style="max-height: 30vh; filter: drop-shadow(0 0 2rem #c05090);"></center>

# Manuel du participant

- [Manuel du participant](#manuel-du-participant)
  - [Installer le serveur](#installer-le-serveur)
  - [Documentation](#documentation)
    - [Contrats d'interfaces](#contrats-dinterfaces)
  - [Tests](#tests)


## Installer le serveur

Pour permettre de tester l'IA, il faut commencer par installer et faire fonctionner le serveur Battlebots en local.

Parmi les éléments qui vous ont été fournis, vous devez avoir le package `battlebots-server-package.zip`

Suivez les procédures [Installation du serveur](serveur/Installation%20du%20serveur.html) et [Configuration du serveur](serveur/Configuration%20du%20serveur.html)


## Documentation

### Contrats d'interfaces

Description des messages envoyés vers le serveur et reçu par celui-ci.

- [Contrats d'interfaces](tech/Contrats%20d'interfaces.html)
- [Contrats d'interfaces - Admin](tech/Contrats%20d'interfaces%20-%20Admin.html)

## Tests

Pour relancer une partie sans avoir à relancer tous les exécutables, faire `Ctrl` + `C` dans le navigateur et taper le mot de passe admin du serveur (`password` par défaut).  Au bout de 5 secondes, le navigateur rechargera la page pour afficher l'écran d'attente. Si ce n'est pas le cas vous pouvez recharger la page manuellement.

N'oubliez pas que pour tester votre IA, vous pouvez démarrer une partie avec de faux joueurs sans IA : [Bots factices](serveur/Configuration%20du%20serveur.html#bots-factices)

---

[⬆️ Retour](#top) - _Manuel du participant_

</div>
