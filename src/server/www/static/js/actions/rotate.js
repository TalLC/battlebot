import {ActionDefinition, actions} from "./actions.js";

function eventwrapper(botState){return botState.ry === undefined? this.ry: botState.ry;}

function actionSelector(botState){return !(botState.ry === undefined);}

function action(rotate_coordinate){
    this.objBot.rotation.y = (-1 * rotate_coordinate)
    this.ry = (-1 * rotate_coordinate)
}

/*    let rotInit = new THREE.Vector3(0, this.ry, 0)
    let rotDest = new THREE.Vector3(0, -1 * rotate_coordinate, 0)
    rotInit.lerp(rotDest, 0.1);
    this.objBot.rotation.setFromVector3(rotInit)
    this.ry = (-1 * rotate_coordinate) */

/**
* @param param
*/
actions.rotate = new ActionDefinition(eventwrapper, actionSelector, action);
