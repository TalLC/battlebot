import GameManager from './gameManager.js';
import Object3DFactory from "./view/object3DFactory.js";
import Bot from "./gameObjects/bot.js"


let instance;

export class BotManager {
    constructor() {
        if (!instance) {
            instance = this;
            this.bots = {};
        }

        return instance;
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
            botData.teamColor,
            botData.shapeName.toLowerCase(),
            botData.shapeSize,
            botData.modelName
        );
        Object3DFactory.createBot3D(this.bots[botData.id]).then(sceneObject => {
            GameManager().viewController.scene.add(sceneObject);
        });
    }

    killBot(id) {
        const bot = this.getBotObjectFromId(id);
        if (bot) bot.kill();
    }

    getBotObjectFromId(id) {
        // On parcourt tous les bots pour chercher l'id demandé
        for(let obj of Object.values(this.bots)) {
            if (obj.id === id) {
                return obj;
            }
        }
    }
}

export default new BotManager();
