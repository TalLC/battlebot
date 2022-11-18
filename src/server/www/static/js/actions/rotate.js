import {ActionDefinition, actions} from "./actions.js";
import * as THREE from '../view/three.module.js';

function eventwrapper(botState){return botState.ry === undefined? this.ry: botState.ry;}

function actionSelector(botState){return !(botState.ry === undefined);}

function action(rotate_coordinate){
    let quat = new THREE.Quaternion(0, 0, 0, 0);
    let rot = new THREE.Euler(0, -1 * rotate_coordinate, 0);
    //let quat = this.objBot.quaternion.clone();
    //let rot = this.objBot.rotation.clone();
    quat.setFromEuler(rot);
    //this.objBot.quaternion.rotateTowards(quat, (this.ry - rotate_coordinate) / 10);
    this.objBot.quaternion.slerp(quat, 0.1);

    this.ry = (-1 * rotate_coordinate);
}


/*    //let quat = new THREE.Quaternion(this.objBot.quaternion.x, this.objBot.quaternion.y, this.objBot.quaternion.z, this.objBot.quaternion.w);
    //let rot = new THREE.Euler(this.objBot.rotation.x, this.objBot.rotation.y, this.objBot.rotation.z, this.objBot.rotation.order);
    let quat = this.objBot.quaternion.clone();
    let rot = this.objBot.rotation.clone();
    rot.y = -1 * rotate_coordinate;
    quat.setFromEuler(rot);
    //this.objBot.quaternion.rotateTowards(quat, (this.ry - rotate_coordinate) / 10);
    this.objBot.quaternion.slerp(quat, 0.1);

    this.ry = (-1 * rotate_coordinate);*/

    /*let rotInit = new THREE.Vector3(0, this.ry, 0)
    let rotDest = new THREE.Vector3(0, -1 * rotate_coordinate, 0)
    rotInit.lerp(rotDest, 0.1);
    this.objBot.rotation.setFromVector3(rotInit)
    this.ry = (-1 * rotate_coordinate)

    this.objBot.rotation.y = (-1 * rotate_coordinate)
    this.ry = (-1 * rotate_coordinate)*/

/**
* @param param
*/
actions.rotate = new ActionDefinition(eventwrapper, actionSelector, action);
