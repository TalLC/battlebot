import BaseWsMessage from "./baseWsMessage.js";
import MapManager from "../mapManager.js";
import Object3DFactory from "../view/object3DFactory.js";

export default class MapCreateMessage extends BaseWsMessage {
    /**
     * Constructeur de la classe MapCreateMessage.
     * @constructor
     * @param {Object} message - Objet de message WS avec les données de la map.
     * @param {Number} message.height - Hauteur de la map.
     * @param {Number} message.width - Largeur de la map.
     * @param {Array} message.tiles_grid - Tableau des cases de la map.
     * @return {MapCreateMessage} - Une instance de MapCreateMessage.
     */
    constructor(message) {
        super();
        this.mapData = {
            height: message.height,
            width: message.width,
            tilesGrid: message.tiles_grid
        };
    }

    /**
     * Exécute le chargement de la map.
     */
    exec() {
        // On attend que le cache 3D soit généré pour créer la map
        Object3DFactory.caching.then(() => MapManager.loadMap(this.mapData));
    }
}
