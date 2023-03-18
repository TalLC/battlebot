import BaseWsMessage from "./baseWsMessage.js";
import BotManager from "../botManager.js";
import Object3DFactory from "../view/object3DFactory.js";

export default class BotCreateMessage extends BaseWsMessage {
    /**
     * Représente un message WebSocket de création de bot
     * @param {Object} message - Les données de création du bot
     * @param {string} message.id - L'identifiant du bot
     * @param {number} message.x - La coordonnée x du bot sur la carte
     * @param {number} message.z - La coordonnée z du bot sur la carte
     * @param {number} message.ry - L'angle de rotation du bot
     * @param {string} message.team_color - La couleur de l'équipe du bot
     * @param {string} message.shape_name - La forme géométrique du bot
     * @param {number} message.shape_size - La taille de la forme géométrique
     * @param {string} [message.model_name='default'] - Le nom du modèle du bot
     */
    constructor(message) {
        super();
        this.botData = {
            id: message.id,
            x: message.x,
            z: message.z,
            ry: -1 * message.ry,
            teamColor: message.team_color,
            shapeName: message.shape_name.toLowerCase(),
            shapeSize: message.shape_size,
            modelName: message.model_name === undefined
                        ? "default"
                        : message.model_name.toLowerCase()
        };
    }

    /**
     * Ajoute un nouveau bot dans le jeu avec les données fournies.
     */
    exec() {
        // On attend que le cache 3D soit généré pour créer les bots
        Object3DFactory.caching.then(() => BotManager.addBot(this.botData));
    }
}
