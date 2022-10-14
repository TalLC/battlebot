import {ActionDefinition, actions} from "./actions.js";

function eventwrapper(botState){return {x:botState.x, z:botState.z};}

function actionSelector(botState){return botState.x && botState.z;}

function action(move_coordinate){
    console.log(this.objBot)
    this.x = move_coordinate.x;
    this.z = move_coordinate.z;
    this.objBot.position.x = move_coordinate.x;
    this.objBot.position.z = move_coordinate.z;
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventwrapper, actionSelector, action);
