import logger from '../../logger.js';
import {ActionDefinition, actions} from "../actions.js";


function eventWrapper(message){return message.id;}

function actionSelector(message){
    return message.msg_type === "GameObjectHurtMessage" && message.id !== undefined;
}

function action(objectId){
    logger.debug("HurtObject", objectId);
    this.hurtObjectFromId(objectId);
}

/**
* @param param
*/
actions.hurt = new ActionDefinition(eventWrapper, actionSelector, action);
