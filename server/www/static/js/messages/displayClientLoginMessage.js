import logger from "../logger.js";
import BaseWsMessage from "./baseWsMessage.js";
import GameManager from "../gameManager.js";
import BotManager from "../botManager.js";
import sendRestMessage from "../utils/rest.js";
import GameConfig from "../config.js";

export default class DisplayClientLoginMessage extends BaseWsMessage {
    /**
     * Message envoyé lorsque le client display se connecte au serveur.
     * @param {Object} message - Objet message reçu du serveur contenant le login_id.
     */
    constructor(message) {
        super();
        this.loginId = message.login_id;
    }

    /**
     * Envoi le message "Prêt" (loginId) au back quand tout est prêt pour démarrer la partie.
     */
    exec() {
        GameManager().loginId = this.loginId;

        // On reçoit la création des bots avant le login du client display
        logger.debug("Waiting for bots to be created");

        this.waitUntilBotsInitialized().then(function (botsCount) {
            // Les bots sont créés, on démarre la partie dans le Back
            if (GameConfig().isDebug) {
                logger.debug(`${botsCount} bots created!`);
                logger.debug("Start game");
            }

            // Affichage du jeu
            GameManager().start();

            // Démarrage du jeu côté Back
            sendRestMessage("PATCH", "/display/clients/action/ready", {
                login_id: GameManager().loginId
            });
        });
    }

    /**
     * Attend la création des bots avant de commencer la partie.
     * @return {Promise} - Promesse résolue avec le nombre de bots en jeu.
     */
    waitUntilBotsInitialized() {
        return new Promise(function (resolve, reject) {
            const intervalId = setInterval(function () {
                // On est prêt lorsque des bots ont rejoins la partie
                const botsCount = Object.keys(BotManager.bots).length;
                if (botsCount >= 1) {
                    clearInterval(intervalId);
                    resolve(botsCount);
                }
            }, 100);
        });
    }
}
