import logger from "../logger.js";
import BotCreateMessage from "./botCreateMessage.js";
import GameInfoMessage from "./gameInfoMessage.js";
import MapCreateMessage from "./mapCreateMessage.js";
import DisplayClientLoginMessage from "./displayClientLoginMessage.js";
import DisplayRefreshMessage from "./displayRefreshMessage.js";

export let updateMessageQueue = [];

/**
 * Classe MessageHandler qui gère les messages entrants et les transmet aux classes de traitement appropriées.
 */
export default class MessageHandler {
    constructor() {}

    /**
     * Méthode de gestion des messages qui analyse et traite les messages entrants.
     * @param {Object} message - L'objet message à traiter.
     * @return {Promise} - Une promesse qui se résout une fois que le message a été traité.
     */
    handle(message) {
        return new Promise((resolve, reject) => {
            // Messages d'actions (update multiples)
            if (message.messages) {
                updateMessageQueue.push(message);
                resolve();
            }
            // Messages de connexion (envois uniques)
            else {
                logger.debug(`Message reçu : ${message.msg_type}`)
                if (message.msg_type) {
                    switch (message.msg_type) {
                        case "BotCreateMessage":
                            new BotCreateMessage(message).exec();
                            resolve();
                            break;
                        case "GameInfoMessage":
                            new GameInfoMessage(message).exec();
                            resolve();
                            break;
                        case "MapCreateMessage":
                            new MapCreateMessage(message).exec();
                            resolve();
                            break;
                        case "DisplayClientLoginMessage":
                            new DisplayClientLoginMessage(message).exec();
                            resolve();
                            break;
                        case "DisplayRefreshMessage":
                            new DisplayRefreshMessage(message).exec();
                            resolve();
                            break;
                        default:
                            reject(`Unknown message type: ${message.msg_type}`);
                    }
                } else {
                    reject(`Unknown message: ${message}`);
                }
            }
        });
    }
}
