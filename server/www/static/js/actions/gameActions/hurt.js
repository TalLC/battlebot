import {ActionDefinition, actions} from "../actions.js";
import GameManager from '../../gameManager.js'

/**
 * Fonction qui crée les paramètres nécessaires pour l'action "hurt".
 * @param {Object} message - Les données reçues par le websocket pour l'action "hurt".
 * @returns {number} L'identifiant de l'objet qui doit être blessé.
 */
function eventWrapper(message) {
    return message.id;
}

/**
 * Fonction qui détermine si l'action "hurt" doit être exécutée.
 * @param {Object} message - Les données reçues par le websocket pour l'action "hurt".
 * @returns {boolean} Un booléen qui détermine si l'action "hurt" doit être exécutée.
 */
function actionSelector(message) {
    return message.msg_type === "GameObjectHurtMessage" && message.id !== undefined;
}

/**
 * Fonction qui permet de blesser un objet dans le GameManager.
 * @param {number} objectId - L'identifiant de l'objet à blesser.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(objectId) {
    GameManager().hurtObjectFromId(objectId);
}

/**
 * Définition de l'action "hurt".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.hurt = new ActionDefinition(eventWrapper, actionSelector, action);
