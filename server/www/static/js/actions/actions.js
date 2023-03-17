export class ActionDefinition{
    constructor(eventwrapper, actionSelector, action){
        this.eventwrapper = eventwrapper;
        this.action = action;
        this.actionSelector = actionSelector;
    }
}

export let actions = {};