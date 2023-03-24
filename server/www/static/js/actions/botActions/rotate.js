import { ActionDefinition, actions } from "../actions.js";

/**
 * Fonction qui crée les paramètres nécessaires pour l'action de rotation.
 * @param {Object} botState - Les données reçues par le websocket pour le bot.
 * @returns {number} La rotation autour de l'axe y.
 */
function eventWrapper(botState) {
    return botState.rotate.ry === undefined ? this.ry : botState.rotate.ry;
}

/**
 * Fonction qui détermine si l'action "rotate" doit être exécutée.
 * @param {Object} botState - Les données reçues par le websocket pour le bot.
 * @returns {boolean} Un booléen qui détermine si l'action doit être exécutée.
 */
function actionSelector(botState) {
    return !(botState.rotate === undefined);
}

/**
 * Fonction qui permet de faire tourner un bot.
 * @param {number} rotateCoordinate - La rotation autour de l'axe y du bot.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(rotateCoordinate) {
    this.sceneObject.rotation.y = -1 * rotateCoordinate;
    this.ry = -1 * rotateCoordinate;
}

/**
 * Définition de l'action "rotate".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.rotate = new ActionDefinition(eventWrapper, actionSelector, action);
