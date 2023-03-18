import "../actions/botActions/botActionDefinition.js"
import {actions} from "../actions/actions.js"
import GameObject from './gameObject.js';


export default class MapObject extends GameObject{
    constructor(id, type, x, y, z, ry, collisionShape, collisionSize, modelName) {
        super(id, type, x, y, z, ry, collisionShape, collisionSize);
        this.modelName = modelName;
        this.sceneObject = null;
    }

    /**
     * Permet l'appel à une action interagissant avec les objets sur la map
     * @param {String} key - Nom de l'action.
     * @param {Object} param - Paramètres de l'action.
     * @return {Void} - N/A
     */
    action(key, param) {
        actions[key].action.call(this, param);
    }
}
