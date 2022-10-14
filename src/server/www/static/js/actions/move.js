import {ActionDefinition, actions} from "./actions.js";
import * as THREE from '../view/three.module.js';

function eventwrapper(botState){return {x:botState.x, z:botState.z};}

function actionSelector(botState){return botState.x && botState.z;}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
 }

async function action(move_coordinate){
    console.log(this.objBot);
    let posInit = new THREE.Vector3(this.x, 0, this.z);
    let posDest = new THREE.Vector3(move_coordinate.x, 0, move_coordinate.z)
    let posCur = new THREE.Vector3(this.x, 0, this.z);
    for(let i = 0.1; i <= 1; i += 0.1){
        posCur.lerpVectors(posInit, posDest, i);
        this.objBot.position.x = posCur.x;
        this.objBot.position.z = posCur.z;
        await sleep(10)
    }

    this.objBot.position.x = posDest.x;
    this.objBot.position.z = posDest.z;


    this.x = move_coordinate.x;
    this.z = move_coordinate.z;
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventwrapper, actionSelector, action);
