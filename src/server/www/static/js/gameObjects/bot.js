import "../actionDefinition.js"
import {actions} from "../actions/actions.js"
import GameObject from './gameObject.js';
import {colorStrToNumber} from '../utils.js'


export default class Bot extends GameObject{
    constructor(construct){
        super(construct.id, "bot", construct.x, 0.5, construct.z, construct.ry);
        this.teamColor = colorStrToNumber(construct.teamColor);
        this.modelName = construct.modelName;
        this.sceneObject = null;

        this.shoot = false;
        this.hit = false;
        this.shieldHide = false;
        this.shieldRaise = false;
        this.enrolled = false;
    }

    /* 
        Fonction : Permet l'appel à une action intéragissant avec le bot (action définit dans actionDefinition.js)
        Param : key -> contient le nom de l'action.
                param -> contient les paramètres nécéssaire à la réalisation de l'action.
        Return : N/A
    */
    action(key,param){
        actions[key].action.call(this, param);
    }

}