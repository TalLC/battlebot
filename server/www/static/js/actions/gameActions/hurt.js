import {ActionDefinition, actions} from "../actions.js";


function eventwrapper(message){return message.id;}

function actionSelector(message){
    return message.msg_type === "GameObjectHurtMessage" && message.id !== undefined;
}

function action(objectId){
    console.log("HurtObject", objectId);
    this.hurtObjectFromId(objectId);
}

/**
* @param param
*/
actions.hurt = new ActionDefinition(eventwrapper, actionSelector, action);
