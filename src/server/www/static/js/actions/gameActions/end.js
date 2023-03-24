import { ActionDefinition, actions } from "../actions.js";

/**
 * Fonction qui crée les paramètres nécessaires pour l'action "end".
 * @param {Object} message - Les données reçues par le websocket pour l'action "end".
 * @returns {string} Le nom du gagnant de la partie.
 */
function eventWrapper(message) {
    return message.winner_name;
}

/**
 * Fonction qui détermine si l'action "end" doit être exécutée.
 * @param {Object} message - Les données reçues par le websocket pour l'action "end".
 * @returns {boolean} Un booléen qui détermine si l'action "end" doit être exécutée.
 */
function actionSelector(message) {
    return (
        message.msg_type === "GameEndMessage" &&
        message.winner_name !== undefined
    );
}

/**
 * Fonction qui permet de terminer la partie.
 * @param {string} winnerName - Le nom du gagnant de la partie.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(winnerName) {
    this.end(winnerName);
}

/**
 * Définition de l'action "end".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.end = new ActionDefinition(eventWrapper, actionSelector, action);
