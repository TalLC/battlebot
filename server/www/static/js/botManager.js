import GameConfig from "./config.js";
import GameManager from "./gameManager.js";
import Object3DFactory from "./view/object3DFactory.js";
import Bot from "./gameObjects/bot.js";

/**
 * Singleton gérant les bots dans le jeu.
 */

let instance;

export class BotManager {
    constructor() {
        if (!instance) {
            instance = this;
            this.bots = {};
        }

        return instance;
    }

    /**
     * Ajoute un bot au jeu.
     * @param {Object} botData - Les informations du bot à ajouter :
     *                             {String} id - L'ID unique du bot.
     *                             {Number} x - La position en x du bot.
     *                             {Number} z - La position en z du bot.
     *                             {Number} ry - La rotation autour de l'axe y du bot.
     *                             {String} teamColor - La couleur de l'équipe à laquelle appartient le bot.
     *                             {String} shapeName - Le nom du modèle 3D représentant le bot.
     *                             {Number} shapeSize - La taille du modèle 3D représentant le bot.
     *                             {String} modelName - Le nom du modèle 3D représentant le bot.
     */
    addBot(botData) {
        this.bots[botData.id] = new Bot(
            botData.id,
            botData.x, botData.z, botData.ry,
            botData.teamColor,
            botData.shapeName.toLowerCase(),
            botData.shapeSize,
            botData.modelName
        );
        Object3DFactory.createBot3D(this.bots[botData.id]).then(sceneObject => {
            GameManager().viewController.scene.add(sceneObject);
        }).then(() => {
            if (GameConfig().isDebug) {
                // Affichage du cône de vision
                this.bots[botData.id].showFov();
            }
        });
    }

    /**
     * Tue le bot spécifié par son ID.
     * @param {String} id - L'ID du bot à tuer.
     */
    killBot(id) {
        const bot = this.getBotObjectFromId(id);
        if (bot) bot.kill();
    }

    /**
     * Renvoie l'objet bot correspondant à l'ID spécifié.
     * @param {String} id - L'ID du bot recherché.
     * @return {Object} - L'objet bot correspondant à l'ID spécifié.
     */
    getBotObjectFromId(id) {
        // On parcourt tous les bots pour chercher l'id demandé
        for (let obj of Object.values(this.bots)) {
            if (obj.id === id) {
                return obj;
            }
        }
    }
}

export default new BotManager();
