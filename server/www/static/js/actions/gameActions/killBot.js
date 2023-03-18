import { ActionDefinition, actions } from "../actions.js";
import BotManager from "../../botManager.js";

/**
 * Fonction qui crée les paramètres nécessaires pour l'action "killBot".
 * @param {Object} message - Les données reçues par le websocket pour l'action "killBot".
 * @returns {number} L'identifiant du bot à supprimer.
 */
function eventWrapper(message) {
    return message.id;
}

/**
 * Fonction qui détermine si l'action "killBot" doit être exécutée.
 * @param {Object} message - Les données reçues par le websocket pour l'action "killBot".
 * @returns {boolean} Un booléen qui détermine si l'action "killBot" doit être exécutée.
 */
function actionSelector(message) {
    return message.msg_type === "BotDeathMessage" && message.id !== undefined;
}

/**
 * Fonction qui permet de supprimer un bot du BotManager.
 * @param {number} objectId - L'identifiant du bot à supprimer.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(objectId) {
    BotManager.killBot(objectId);
}

/**
 * Définition de l'action "killBot".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.killBot = new ActionDefinition(eventWrapper, actionSelector, action);
