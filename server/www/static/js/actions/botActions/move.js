import { ActionDefinition, actions } from "../actions.js";
import * as TWEEN from "tween";

/**
 * Fonction qui crée les paramètres nécessaires pour l'action "move".
 * @param {Object} botState - Les données reçues par le websocket pour le bot.
 * @returns {Object} Un dictionnaire contenant les positions en x et en z "final" du bot.
 */
function eventWrapper(botState) {
    return {
        x: botState.move.x === undefined ? this.x : botState.move.x,
        z: botState.move.z === undefined ? this.z : botState.move.z
    };
}

/**
 * Fonction qui détermine si l'action "move" doit être exécutée.
 * @param {Object} botState - Les données reçues par le websocket pour le bot.
 * @returns {boolean} Un booléen qui détermine si l'action "move" doit être exécutée.
 */
function actionSelector(botState) {
    return !(botState.move === undefined);
}

/**
 * Fonction qui permet de déplacer un bot.
 * @param {Object} moveCoordinate - Un dictionnaire avec les informations nécessaires au mouvement du bot en x et en z.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(moveCoordinate) {
    new TWEEN.Tween({
        x: this.sceneObject.position.x,
        z: this.sceneObject.position.z
    })
        .to({ x: moveCoordinate.x, z: moveCoordinate.z }, 100)
        .easing(TWEEN.Easing.Linear.None)
        .onUpdate((coords) => {
            // this.sceneObject.position.x = coords.x;
            // this.sceneObject.position.z = coords.z;
            this.x = coords.x;
            this.z = coords.z;
        })
        .start();
}

/**
 * Définition de l'action "move".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.move = new ActionDefinition(eventWrapper, actionSelector, action);
