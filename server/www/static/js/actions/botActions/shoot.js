import { ActionDefinition, actions } from "../actions.js";
import GameManager from "../../gameManager.js";
import BotManager from "../../botManager.js";

/**
 * Fonction qui crée les paramètres nécessaires pour l'action "shoot".
 * @param {Object} botState - Les données reçues par le websocket pour l'action "shoot".
 * @returns {Object} Un dictionnaire contenant l'identifiant du bot et les coordonnées des cibles du tir.
 */
function eventWrapper(botState) {
    return { id: botState.id, targets: botState.shoot };
}

/**
 * Fonction qui détermine si l'action "shoot" doit être exécutée.
 * @param {Object} botState - Les données reçues par le websocket pour l'action "shoot".
 * @returns {boolean} Un booléen qui détermine si l'action "shoot" doit être exécutée.
 */
function actionSelector(botState) {
    return !(botState.shoot === undefined);
}

/**
 * Fonction qui permet d'afficher le tir du bot.
 * @param {Object} parameters - Un dictionnaire contenant l'identifiant du bot et les coordonnées des cibles du tir.
 * @returns {void} Cette fonction ne retourne rien.
 */
function action(parameters) {
    const bot = BotManager.bots[parameters.id];

    for (let target of parameters.targets) {
        if (!target.id) {
            GameManager().viewController.shootTo(bot, target);
        } else {
            const targetObject = GameManager().getGameObjectFromId(target.id);
            if (targetObject) {
                GameManager().viewController.shootTo(bot, targetObject.coordinates2D);
            } else {
                console.error(`L'objet ayant pour ID ${target.id} n'a pas été trouvé`);
            }
        }
    }
}

/**
 * Définition de l'action "shoot".
 * @type {ActionDefinition}
 * @param {Object} param - Les paramètres de l'action.
 */
actions.shoot = new ActionDefinition(eventWrapper, actionSelector, action);
