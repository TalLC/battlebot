import {ActionDefinition, actions} from "./actions.js";

function eventwrapper(botState){return {x:botState.x, z:botState.z};}

function actionSelector(botState){return botState.x && botState.z;}

function action(move_coordinate){
    console.log(move_coordinate);
    //let dist = THREE.Vector3(this.x, 0, this.z).distanceTo(THREE.Vector3(move_coordinate[0], 0, move_coordinate[1]));
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventwrapper, actionSelector, action);
