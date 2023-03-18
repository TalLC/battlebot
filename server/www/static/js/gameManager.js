import GameConfig from './config.js';
import "./actions/gameActions/gameActionDefinition.js"
import { actions } from "./actions/actions.js"
import View3DController from "./view/view3DController.js";
import Object3DFactory from "./view/object3DFactory.js";
import Bot from "./gameObjects/bot.js"
import MapManager from "./mapManager.js"


let instance;
export default function getInstance() {
    return instance;
};

export function initGameManager() {
    instance = new GameManager();
};

class GameManager {
    constructor() {
        this.viewController = new View3DController(this, "view-container");
        this.mapManager = new MapManager(this);
        this.loginId;
        this.bots = {};

        /* Page d'accueil */
        // Nombre de joueurs
        const startgameContainer = document.getElementById("startgame-container");
        let startgameMessagesRules = startgameContainer.querySelector("#startgame-messages-rules");
        startgameMessagesRules.innerHTML = `LA PARTIE DÉMARRE À PARTIR DE ${GameConfig().maxPlayers} BOTS ET SE TERMINE LORSQU'IL NE RESTE QU'1 ÉQUIPE EN VIE`;
        
        // Scroll text
        const scrollText = document.getElementById("startgame-scroll-text");
        fetch('static/txt/scrolling-text.txt')
            .then((response) => response.text())
            .then((data) => {
                scrollText.innerHTML = data;
                scrollText.style.height = scrollText.scrollHeight;
            });

        /* Endgame */
        this.endgameContainer = document.getElementById("endgame-container");
        this.endgameModal = document.getElementById("endgame-modal");
        this.endgameMessageL1 = this.endgameModal.querySelector("#endgame-message-l1");
    }

    get allGameObjects() {
        return {
            ...this.bots,
            ...this.mapManager.mapObjects
        };
    }

    /* 
        Fonction : Permet l'appel à une action interagissant avec le jeu
        Param : key -> contient le nom de l'action.
                param -> contient les paramètres nécessaire à la réalisation de l'action.
        Return : N/A
    */
    action(key,param){
        actions[key].action.call(this, param);
    }

    render() {
        for (let bot of Object.values(this.bots)) {
            bot.render();
        }

        this.viewController.render();
    }

    start() {
        // Masquer la page d'attente
        const startgameContainer = document.getElementById("startgame-container");
        const startgameScrollContainer = document.getElementById("startgame-scroll-container");
        startgameScrollContainer.hidden = true;
        startgameContainer.hidden = true;

        // Suppression du défilement de texte
        const startgameScrollText = startgameScrollContainer.querySelector("#startgame-scroll-text");
        startgameScrollText.classList.remove("vertical-scrolling-text");

        this.viewController.start();
    }

    end(winnerName) {
        // Définition du nom du gagnant
        const endgameModalTemplate = document.getElementById("endgame-modal");
        const endgameMessageL1 = endgameModalTemplate.querySelector("#endgame-message-l1");
        endgameMessageL1.innerHTML = winnerName;

        // Affichage du message de fin
        const endgameModal = new bootstrap.Modal(endgameModalTemplate);
        endgameModal.show();
    }

    /*
        Fonction : Permet la réalisation des actions pour un des bots, reçu dans un appel websocket.
        Param : message -> correspond aux données pour un bot, reçu dans un appel websocket.
        Return : N/A
    */
    doAction(message){
        // Création d'une promise vide
        let promise = Promise.resolve();

        //logger.debug(message.msg_type);
        
        if (message.msg_type === "BotUpdateMessage") {
            // On vérifie si le bot existe
            if (this.bots[message.id] && this.bots[message.id].sceneObject) {
                
                // Parcours des actions enregistrées
                for(let actionDef in actions) {
    
                    // Choix de l'action à effectuer suivant les arguments trouvés dans le message
                    let selected = actions[actionDef].actionSelector(message);
                    
                    if(selected){
                        let paramAction = actions[actionDef].eventWrapper(message);
                        promise = promise.then(() => {
                            this.bots[message.id].action(actionDef, paramAction);
                        });
                    }
                }
            }
        } else {
            for (let actionDef in actions) {
    
                // Choix de l'action à effectuer suivant les arguments trouvés dans le message
                let selected = actions[actionDef].actionSelector(message);
    
                if (selected){
                    let paramAction = actions[actionDef].eventWrapper(message);
                    promise = promise.then(() => {
                        this.action(actionDef, paramAction);
                    });
                }
            }
        }
    
        return promise;
    }
    

    hurtObjectFromId(id) {
        // Récupération du GameObject à partir de l'id
        const obj = this.getGameObjectFromId(id);

        // Affichage du hit
        if (obj) this.viewController.showHurtMessageForObject(obj);
    }

    destroyGameObjectFromId(id) {
        // Récupération du GameObject à partir de l'id
        const obj = this.getGameObjectFromId(id);

        // Appel du destructeur de l'objet
        if (obj) obj.dispose();
    }
    
    removeGameObjectFromId(id) {
        // Supprime un GameObject de son dictionnaire
        delete this.mapManager.mapObjects[id];
        delete this.bots[id];
    }

    removeGameObject(gameObject) {
        // Supprime un GameObject de son dictionnaire
        this.removeGameObjectFromId(gameObject.id);
    }

    /*
        Fonction : Permet la création de Bots dans le jeu.
        Param : id -> ID unique du Bot
                x -> Position en x
                z -> Position en z
                ry -> Rotation autour de l'axe y
                team_color -> Couleur de l'équipe à laquelle appartient le Bot
                model_name -> Nom du modèle 3D représentant le bot
        Return : N/A
    */
    addBot(botData) {
        this.bots[botData.id] = new Bot(
            botData.id,
            botData.x, botData.z, botData.ry,
            botData.team_color,
            botData.shape_name.toLowerCase(),
            botData.shape_size,
            botData.model_name
        );
        Object3DFactory.createBot3D(this.bots[botData.id]).then(sceneObject => {
            this.viewController.scene.add(sceneObject);
        });
    }

    killBot(id) {
        const bot = this.getGameObjectFromId(id);
        if (bot) bot.kill();
    }


    /*
        Fonction : Retrouve un GameObject à partir d'un objet de la scène ThreeJs.
        Param : sceneObject -> Objet de la scène ThreeJs
                checkFor -> Type de GameObject à trouver
        Return : GameObject
    */
    getGameObjectFromSceneObject(sceneObject, checkFor) {
        if (checkFor === "bot") {
            for(let obj of Object.values(this.bots)) {
                if (obj.type === "bot" && obj.sceneObject === sceneObject) {
                    return obj;
                }
            }
        } else if (checkFor === "tileObject" || checkFor === "tile") {
            for(let obj of Object.values(this.mapManager.mapObjects)) {
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

    getGameObjectFromId(id) {
        // On parcourt tous les objets de la map pour chercher l'id demandé
        for(let obj of Object.values(this.allGameObjects)) {
            if (obj.id === id) {
                return obj;
            }
        }
    }

}

