import "../actions/botActions/botActionDefinition.js"
import {actions} from "../actions/actions.js"
import GameObject from './gameObject.js';


export default class MapObject extends GameObject{
    constructor(id, type, x, y, z, ry, collisionShape, collisionSize, modelName) {
        super(id, type, x, y, z, ry, collisionShape, collisionSize);
        this.modelName = modelName;
        this.sceneObject = null;
    }

    /* 
        Fonction : Permet l'appel à une action intéragissant avec les objets sur la map (action non définit pour l'instant)
        Param : key -> contient le nom de l'action.
                param -> contient les paramètres nécéssaire à la réalisation de l'action.
        Return : N/A
    */
    action(key,param){
        actions[key].action.call(this, param);
    }
}
