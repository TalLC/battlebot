import "../actionDefinition.js"
import {actions} from "../actions/actions.js"
import GameObject from './gameObject.js';


export default class MapObject extends GameObject{
    constructor(construct){
        super(construct.id, construct.type, construct.x, construct.y, construct.z, construct.ry);
        this.modelName = construct.modelName;
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
