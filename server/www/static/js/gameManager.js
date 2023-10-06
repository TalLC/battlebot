import GameConfig from "./config.js";
import "./actions/gameActions/gameActionDefinition.js";
import { actions } from "./actions/actions.js";
import sendRestMessage from "./utils/rest.js";
import View3DController from "./view/view3DController.js";
import MapManager from "./mapManager.js";
import BotManager from "./botManager.js";
import logger from "./logger.js";

/**
 * Singleton gérant le jeu.
 * La config du jeu doit être initialisée avant de créer la 1ère instance de GameManager.
 */

let instance;

export default function getInstance() {
    return instance;
}

/**
 * Initialise le GameManager
 */
export function initGameManager() {
    instance = new GameManager();
}

class GameManager {
    /**
     * Constructeur de GameManager
     */
    constructor() {
        // Crée le contrôleur de vue 3D et cache la page d'attente
        this.viewController = new View3DController(this, "view-container");
        this.loginId;

        /* Page d'accueil */
        this.waitgameContainer = document.getElementById("choice-game-container");
        const startbouton = this.waitgameContainer.querySelector("#choice-game-start-button");
        startbouton.onclick = this.testStart.bind(this);
        /* Page d'attente */
        // Nombre de joueurs
        this.startgameContainer = document.getElementById("startgame-container");
        const startgameMessagesRules = this.startgameContainer.querySelector("#startgame-messages-rules");
        startgameMessagesRules.innerHTML = `LA PARTIE DÉMARRE À PARTIR DE ${GameConfig().maxPlayers} BOTS ET SE TERMINE LORSQU'IL NE RESTE QU'1 ÉQUIPE EN VIE`;

        // Scroll text
        const scrollText = document.getElementById("startgame-scroll-text");
        fetch("static/txt/scrolling-text.txt")
            .then((response) => response.text())
            .then((data) => {
                scrollText.innerHTML = data;
                scrollText.style.height = scrollText.scrollHeight;
            });

        /* Endgame */
        this.endgameContainer = document.getElementById("endgame-container");
        this.endgameModal = document.getElementById("endgame-modal");
        this.endgameMessageL1 = this.endgameModal.querySelector("#endgame-message-l1");


        /* Reset */
        window.onkeydown = this.reset.bind(this);
    }

    /**
     * Retourne la liste de tous les objets de jeu
     * @returns {object} - Liste de tous les objets de jeu
     */
    get allGameObjects() {
        return {
            ...BotManager.bots,
            ...MapManager.mapObjects
        };
    }

    /**
     * Appelle une action de jeu
     * @param {string} key - Le nom de l'action
     * @param {object} param - Les paramètres nécessaires à l'action
     */
    action(key, param) {
        actions[key].action.call(this, param);
    }

    /**
     * Met à jour le rendu des GameObjects qui en ont besoin.
     */
    render() {
        for (let bot of Object.values(BotManager.bots)) {
            bot.render();
        }

        this.viewController.render();
    }

    testStart() {
        const maplist = document.getElementById("choice-game-maplist");
        Array.from(maplist.children).forEach(button => {
            if(button.classList.contains("active")){
                const mapSelectId = button.value;
                this.selectMap(mapSelectId);
                return;
            }
        })
    }

    selectMap(mapSelectId) {
        //envoi de info de lancement de partie au back
        const password = GameConfig().isDebug ? GameConfig().debugAdminPassword : prompt("Mot de passe administrateur", "")
        sendRestMessage("POST", `/game/maps/${mapSelectId}/select`, {
            api_password: password
        }).then((reponse) => {
            if(reponse.ok){
                sendRestMessage("POST", `/game/action/new`, {
                    api_password: password
                }).then((reponse) => {
                    if(reponse.ok){
                        //Masquer la page de selection
                        this.waitgameContainer.hidden = true;

                        //Affichage de la page d'attente
                        this.startgameContainer.hidden = false;
                    }
                    else{
                        console.error("Mauvaise réponse suite au lancement de la partie");
                    }
                });
            }
            else{
                console.error("Mauvaise réponse suite à la selection de map");
            }
        }).catch(function (error) {
            console.error("Il y a eu un problème avec l'opération fetch : " + error.message);
        });
    }

    /**
     * Masque l'écran d'attente et affiche le jeu.
     */
    start() {
        // Masquer la page d'attente
        const startgameScrollContainer = document.getElementById("startgame-scroll-container");
        startgameScrollContainer.hidden = true;
        this.startgameContainer.hidden = true;

        // Suppression du défilement de texte
        const startgameScrollText = startgameScrollContainer.querySelector("#startgame-scroll-text");
        startgameScrollText.classList.remove("vertical-scrolling-text");
        
        // Affichage du menu latéral
        const sideMenuContainer = document.getElementById("menu-container");
        sideMenuContainer.hidden = false;
        
        // Affichage du canvas ThreeJS
        const mainCanvasContainer = document.getElementById("view-container");
        mainCanvasContainer.hidden = false;

        this.viewController.start();
    }

    /**
     * Reset la partie.
     * @param {KeyboardEvent} event - Les touches appuyées
     */
    reset(event) {
        if (event.ctrlKey === GameConfig().resetCtrlKey
            && event.altKey === GameConfig().resetAltKey
            && event.shiftKey === GameConfig().resetShiftKey
            && event.key === GameConfig().resetKey) {
            
            // On demande un mot de passe pour reset la partie seulement en mode Prod
            // En mode debug on donne le mdp debug
            sendRestMessage("POST", `/game/action/reset`, {
                api_password: GameConfig().isDebug ?
                GameConfig().debugAdminPassword : prompt("Reset de la partie - Mot de passe administrateur", "")
            });
        }
    }

    /**
     * Affiche l'écran de fin de partie et bloque les contrôles.
     * @param {string} winnerName - Le nom du gagnant
     */
    end(winnerName) {
        // Définition du nom du gagnant
        const endgameModalTemplate = document.getElementById("endgame-modal");
        const endgameMessageL1 = endgameModalTemplate.querySelector("#endgame-message-l1");
        endgameMessageL1.innerHTML = winnerName;

        // Affichage du message de fin
        const endgameModal = new bootstrap.Modal(endgameModalTemplate);
        endgameModal.show();
    }

    /**
     * Permet la réalisation des actions pour un des bots, reçu dans un appel websocket.
     * @param {Object} message - Les données pour un bot, reçu dans un appel websocket.
     * @returns {Promise} - Une promesse qui se résout lorsque toutes les actions ont été effectuées.
     */
    doAction(message) {
        // Création d'une promise vide
        let promise = Promise.resolve();

        if (message.msg_type === "BotUpdateMessage") {
            // On vérifie si le bot existe
            if (BotManager.bots[message.id] && BotManager.bots[message.id].sceneObject) {
                // Parcours des actions enregistrées
                for (let actionDef in actions) {
                    // Choix de l'action à effectuer suivant les arguments trouvés dans le message
                    let selected = actions[actionDef].actionSelector(message);

                    if (selected) {
                        let paramAction = actions[actionDef].eventWrapper(message);
                        promise = promise.then(() => {
                            BotManager.bots[message.id].action(actionDef, paramAction);
                        });
                    }
                }
            }
        } else {
            for (let actionDef in actions) {
                // Choix de l'action à effectuer suivant les arguments trouvés dans le message
                let selected = actions[actionDef].actionSelector(message);

                if (selected) {
                    let paramAction = actions[actionDef].eventWrapper(message);
                    promise = promise.then(() => {
                        this.action(actionDef, paramAction);
                    });
                }
            }
        }

        return promise;
    }

    /**
     * Affiche l'animation de coup sur un GameObject à partir de son ID.
     * @param {string} id - L'identifiant du GameObject.
     */
    hurtObjectFromId(id) {
        // Récupération du GameObject à partir de l'id
        const obj = this.getGameObjectFromId(id);

        // Affichage du hit
        if (obj) this.viewController.showHurtMessageForObject(obj);
    }

    /**
     * Détruit un GameObject à partir de son ID.
     * L'objet supprime le modèle 3D et attend un peu avant de se supprimer du dictionnaire.
     * @param {string} id - L'identifiant du GameObject.
     */
    destroyGameObjectFromId(id) {
        // Récupération du GameObject à partir de l'id
        const obj = this.getGameObjectFromId(id);

        // Appel du destructeur de l'objet
        if (obj) obj.dispose();
    }

    /**
     * Supprime un GameObject de son dictionnaire à partir de son ID.
     * @param {string} id - L'identifiant du GameObject.
     */
    removeGameObjectFromId(id) {
        // Supprime un GameObject de son dictionnaire
        delete MapManager.mapObjects[id];
        delete BotManager.bots[id];
    }

    /**
     * Supprime un GameObject de son dictionnaire.
     * @param {Object} gameObject - Le GameObject à supprimer.
     */
    removeGameObject(gameObject) {
        // Supprime un GameObject de son dictionnaire
        this.removeGameObjectFromId(gameObject.id);
    }

    /**
     * Retrouve un GameObject à partir d'un objet de la scène ThreeJs.
     * @param {Object} sceneObject - L'objet de la scène ThreeJs.
     * @param {string} checkFor - Le type de GameObject à trouver.
     * @returns {Object} - Le GameObject trouvé.
     */
    getGameObjectFromSceneObject(sceneObject, checkFor) {
        if (checkFor === "bot") {
            for (let obj of Object.values(BotManager.bots)) {
                if (obj.sceneObject === sceneObject) {
                    return obj;
                }
            }
        } else if (checkFor === "tileObject" || checkFor === "tile") {
            for (let obj of Object.values(MapManager.mapObjects)) {
                if (obj.sceneObject) {
                    if (obj.type === checkFor) {
                        if (obj.sceneObject === sceneObject) {
                            return obj;
                        }
                        if (obj.sceneObject === sceneObject.parent) {
                            return obj;
                        }
                    }
                }
            }
        }
    }

    /**
     * Retrouve un GameObject à partir de son ID.
     * @param {string} id - L'identifiant du GameObject.
     */
    getGameObjectFromId(id) {
        // On parcourt tous les objets de la map pour chercher l'id demandé
        for (let obj of Object.values(this.allGameObjects)) {
            if (obj.id === id) {
                return obj;
            }
        }
    }
}
