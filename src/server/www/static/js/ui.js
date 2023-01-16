import sendRestMessage from './rest.js'


export default class Ui {

    constructor(game, uiContainerId) {
        this.gameManager = game;
        const uiContainer = document.getElementById(uiContainerId);

        const buttonForceStart = uiContainer.querySelector("#ui-button-force-start");
        buttonForceStart.onclick = this.debug_forceStartGame.bind(this);
        
        const buttonAddBot = uiContainer.querySelector("#ui-button-add-bot");
        buttonAddBot.onclick = this.debug_addBot.bind(this);
    }

    debug_forceStartGame() {
        sendRestMessage('PATCH', '/game/action/start', {"api_password": "password"});
    }

    debug_addBot() {
        sendRestMessage('PATCH', '/bots/action/add', {"api_password": "password"});
    }

}