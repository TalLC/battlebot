import {ActionDefinition, actions} from "../actions.js";


function eventwrapper(message){return message.id;}

function actionSelector(message){
    return message.msg_type === "BotDeathMessage" && message.id !== undefined;
}

function action(objectId){
    this.killBot(objectId);
}

/**
* @param param
*/
actions.killBot = new ActionDefinition(eventwrapper, actionSelector, action);
