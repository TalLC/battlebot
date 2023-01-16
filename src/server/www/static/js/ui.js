import sendRestMessage from './rest.js'


export default class Ui {

    constructor(game, uiContainerId) {
        this.gameManager = game;
        const uiContainer = document.getElementById(uiContainerId);

        const buttonForceStart = uiContainer.querySelector("#ui-button-force-start");
        buttonForceStart.onclick = this.debug_forceStartGame.bind(this);
        
        const buttonAddBot = uiContainer.querySelector("#ui-button-add-bot");
        buttonAddBot.onclick = this.debug_addBot.bind(this);
        
        const buttonKillBot = uiContainer.querySelector("#ui-button-kill-bot");
        buttonKillBot.onclick = this.debug_killBot.bind(this);
    }

    debug_forceStartGame() {
        sendRestMessage('PATCH', '/game/action/start', {"api_password": "password"});
    }

    debug_addBot() {
        sendRestMessage('PATCH', '/bots/action/add', {"api_password": "password"});
    }

    debug_killBot() {
        let botId = prompt("ID du bot :", "0-0-0-0-0");
        if (botId !== null && botId !== "") {
            sendRestMessage('PATCH', `/bots/${botId}/action/kill`, {"api_password": "password"});
        }
    }

}