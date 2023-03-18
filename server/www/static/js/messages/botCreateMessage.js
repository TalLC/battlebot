import BaseWsMessage from './baseWsMessage.js'
import GameManager from '../gameManager.js';
import Object3DFactory from '../view/object3DFactory.js';


export default class BotCreateMessage extends BaseWsMessage {
    constructor(message){
        super();
        this.botData = {
            id: message.id,
            x: message.x, z: message.z, ry: -1 * message.ry,
            team_color: message.team_color,
            shape_name: message.shape_name.toLowerCase(),
            shape_size: message.shape_size,
            model_name: message.model_name === undefined? 'default' : message.model_name.toLowerCase()
        };
    }

    exec() {
        // On attend que le cache 3D soit généré pour créer les bots
        Object3DFactory.caching.then(() => GameManager().addBot(this.botData));
    }
}
