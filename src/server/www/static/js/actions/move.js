import {ActionDefinition, actions} from "./actions.js";
import * as THREE from 'three';

function eventwrapper(botState){return {x: botState.x === undefined? this.x: botState.x, z: botState.x === undefined? this.z: botState.z};}

function actionSelector(botState){return botState.x || botState.z;}

function action(move_coordinate){
    let posDest = new THREE.Vector3(move_coordinate.x, 0.5, move_coordinate.z)

    this.objBot.position.lerp(posDest, 0.1);
    this.x = posDest.x;
    this.z = posDest.z;
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventwrapper, actionSelector, action);
