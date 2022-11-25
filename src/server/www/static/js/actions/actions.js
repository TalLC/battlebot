export class ActionDefinition{
    eventwrapper;
    action;
    actionSelector;
    constructor(eventwrapper, actionSelector, action){
        this.eventwrapper = eventwrapper;
        this.action = action;
        this.actionSelector = actionSelector;
    }
}

export let actions = {};