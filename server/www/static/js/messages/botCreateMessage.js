import BaseWsMessage from './baseWsMessage.js'
import BotManager from '../botManager.js';
import Object3DFactory from '../view/object3DFactory.js';


export default class BotCreateMessage extends BaseWsMessage {
    constructor(message){
        super();
        this.botData = {
            id: message.id,
            x: message.x, z: message.z, ry: -1 * message.ry,
            teamColor: message.team_color,
            shapeName: message.shape_name.toLowerCase(),
            shapeSize: message.shape_size,
            modelName: message.model_name === undefined? 'default' : message.model_name.toLowerCase()
        };
    }

    exec() {
        // On attend que le cache 3D soit généré pour créer les bots
        Object3DFactory.caching.then(() => BotManager.addBot(this.botData));
    }
}
