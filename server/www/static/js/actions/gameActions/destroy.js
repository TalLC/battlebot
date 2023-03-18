import {ActionDefinition, actions} from "../actions.js";


function eventWrapper(message){return message.id;}

function actionSelector(message){
    return message.msg_type === "GameObjectDestroyMessage" && message.id !== undefined;
}

function action(objectId){
    this.destroyGameObjectFromId(objectId);
}

/**
* @param param
*/
actions.destroy = new ActionDefinition(eventWrapper, actionSelector, action);
