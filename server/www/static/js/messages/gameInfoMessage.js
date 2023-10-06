import BaseWsMessage from "./baseWsMessage.js";
import { initGameManager } from "../gameManager.js";
import MapSelector from "../mapSelector.js";
import { initGameConfig } from "../config.js";
import Animator from "../view/animator.js";

export default class GameInfoMessage extends BaseWsMessage {
    constructor(message) {
        super();

        /**
         * Informations du jeu
         * @typedef {Object} GameInfo
         * @property {Boolean} isDebug - Indique si le jeu est en mode debug.
         * @property {String} maps - Liste des noms et id des maps disponibles.
         * @property {Number} maxPlayers - Le nombre maximum de joueurs autorisés.
         */

        /** @type {GameInfo} */
        this.gameInfo = {
            isDebug: message.is_debug,
            maps: message.maps,
            maxPlayers: message.max_players
        };
    }

    /**
     * Initialise la configuration et le gestionnaire de jeu, et déclenche la boucle d'update du visuel ThreeJs.
     * @returns {void}
     */
    exec() {
        // Création de la config du jeu
        initGameConfig(this.gameInfo);

        // Création des boutons
        MapSelector.createChoiceGameMapButtons(this.gameInfo.maps);

        // On a besoin de la config du jeu pour déclarer le GameManager
        initGameManager();

        // Création de l'Animator qui va consulter les updateMessages
        new Animator();
    }
}
