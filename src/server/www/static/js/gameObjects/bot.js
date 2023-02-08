import "../actions/botActions/botActionDefinition.js"
import {actions} from "../actions/actions.js"
import GameObject from './gameObject.js';
import {colorStrToNumber} from '../utils/utils.js'
import * as THREE from 'three';


export default class Bot extends GameObject{
    constructor(id, x, z, ry, teamColor, collisionShape, collisionSize, modelName) {
        super(id, "bot", x, 0.5, z, ry,  collisionShape, collisionSize);
        this.teamColor = colorStrToNumber(teamColor);
        this.modelName = modelName;
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

    kill() {
        this.applyMaterial(
            new THREE.MeshPhongMaterial(
                {
                    color: 0x424242,
                    transparent: true,
                    opacity: 0.7
                }
            )
        );
    }

}