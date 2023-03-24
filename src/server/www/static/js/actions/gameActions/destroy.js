import { ActionDefinition, actions } from "../actions.js";

/**
 * Fonction qui crée les paramètres nécessaires pour l'action "destroy".
 * @param {Object} message - Les données reçues par le websocket pour l'action "destroy".
 * @returns {number} L'identifiant de l'objet qui doit être détruit.
 */
function eventWrapper(message) {
    return message.id;
}

/**
 * Fonction qui détermine si l'action "destroy" doit être exécutée.
 * @param {Object} message - Les données reçues par le websocket pour l'action "destroy".
 * @returns {boolean} Un booléen qui détermine si l'action "destroy" doit être exécutée.
 */
function actionSelector(message) {
    return (
        message.msg_type === "GameObjectDestroyMessage" &&
        message.id !== undefined
    );
}

/**
 * Fonction qui permet de détruire un objet dans le jeu.
 * @param {number} objectId - L'identifiant de l'objet à détruire.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(objectId) {
    this.destroyGameObjectFromId(objectId);
}

/**
 * Définition de l'action "destroy".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.destroy = new ActionDefinition(eventWrapper, actionSelector, action);
