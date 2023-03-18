import BaseWsMessage from "./baseWsMessage.js";
import { initGameManager } from "../gameManager.js";
import { initGameConfig } from "../config.js";
import GameManager from "../gameManager.js";

export default class GameInfoMessage extends BaseWsMessage {
    constructor(message) {
        super();

        /**
         * Informations du jeu
         * @typedef {Object} GameInfo
         * @property {Boolean} isDebug - Indique si le jeu est en mode debug.
         * @property {String} mapId - L'ID de la carte du jeu.
         * @property {Number} maxPlayers - Le nombre maximum de joueurs autorisés.
         */

        /** @type {GameInfo} */
        this.gameInfo = {
            isDebug: message.is_debug,
            mapId: message.map_id,
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

        // On a besoin de la config du jeu pour déclarer le GameManager
        initGameManager();

        // Déclenchement de la boucle d'update du visuel ThreeJs
        GameManager().viewController.animate();
    }
}