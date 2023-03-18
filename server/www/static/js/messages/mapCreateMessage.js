import BaseWsMessage from './baseWsMessage.js'
import GameManager from '../gameManager.js';
import Object3DFactory from '../view/object3DFactory.js';


export default class MapCreateMessage extends BaseWsMessage {
    constructor(message){
        super();
        this.mapData = {
            height: message.height,
            width: message.width,
            tilesGrid: message.tiles_grid,
        };
    }

    exec() {
        // On attend que le cache 3D soit généré pour créer la map
        Object3DFactory.caching.then(() => GameManager().mapManager.loadMap(this.mapData));
    }
}
