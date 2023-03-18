import {ActionDefinition, actions} from "../actions.js";


function eventWrapper(message){return message.id;}

function actionSelector(message){
    return message.msg_type === "BotDeathMessage" && message.id !== undefined;
}

function action(objectId){
    this.killBot(objectId);
}

/**
* @param param
*/
actions.killBot = new ActionDefinition(eventWrapper, actionSelector, action);
