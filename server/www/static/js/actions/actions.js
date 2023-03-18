/**
 * Une classe représentant une définition d'action, avec une fonction pour créer les paramètres, une pour déterminer si l'action doit être exécutée et une pour effectuer l'action.
 * @class
 * @classdesc Cette classe est utilisée pour créer des actions qui peuvent être exécutées par le jeu. Elle contient des fonctions pour créer les paramètres, déterminer si l'action doit être exécutée et effectuer l'action elle-même.
 * @property {Function} eventWrapper - Une fonction qui crée les paramètres nécessaires à l'action.
 * @property {Function} actionSelector - Une fonction qui détermine si l'action doit être exécutée.
 * @property {Function} action - Une fonction qui effectue l'action.
 */
export class ActionDefinition {
    constructor(eventWrapper, actionSelector, action) {
        this.eventWrapper = eventWrapper;
        this.action = action;
        this.actionSelector = actionSelector;
    }
}

/**
 * Un objet contenant toutes les actions du jeu.
 * @type {Object}
 * @property {ActionDefinition} [nomDeLAction] - Une définition d'action pour l'action nomDeLAction.
 */
export let actions = {};
