import {ActionDefinition, actions} from "../actions.js";


function eventWrapper(message){return message.winner_name;}

function actionSelector(message){
    return message.msg_type === "GameEndMessage" && message.winner_name !== undefined;
}

function action(winnerName){
    this.end(winnerName);
}

/**
* @param param
*/
actions.end = new ActionDefinition(eventWrapper, actionSelector, action);
