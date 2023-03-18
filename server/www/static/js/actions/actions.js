export class ActionDefinition{
    constructor(eventWrapper, actionSelector, action){
        this.eventWrapper = eventWrapper;
        this.action = action;
        this.actionSelector = actionSelector;
    }
}

export let actions = {};