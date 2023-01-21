import sendRestMessage from './rest.js'


export default class DebugUi {

    constructor(debug) {
        this.debug = debug;

        // Header
        const headerContainer = document.getElementById("header-container");

        const buttonForceStart = headerContainer.querySelector("#header-button-force-start");
        buttonForceStart.onclick = this.debug_forceStartGame.bind(this);
        
        const buttonAddBot = headerContainer.querySelector("#header-button-add-bot");
        buttonAddBot.onclick = this.debug_addBot.bind(this);
        
        const buttonKillBot = headerContainer.querySelector("#header-button-kill-bot");
        buttonKillBot.onclick = this.debug_killBot.bind(this);

        // Remote
        const remoteContainer = document.getElementById("remote-container");
        
        const buttonRemoteStartMove = remoteContainer.querySelector("#button-remote-up");
        buttonRemoteStartMove.onclick = this.debug_remoteStartMove.bind(this);
        
        const buttonRemoteStopMove = remoteContainer.querySelector("#button-remote-stop");
        buttonRemoteStopMove.onclick = this.debug_remoteStopMove.bind(this);
        
        const buttonRemoteStartTurnLeft = remoteContainer.querySelector("#button-remote-left");
        buttonRemoteStartTurnLeft.onclick = this.debug_remoteStartTurnLeft.bind(this);
        
        const buttonRemoteStartTurnRight = remoteContainer.querySelector("#button-remote-right");
        buttonRemoteStartTurnRight.onclick = this.debug_remoteStartTurnRight.bind(this);
        
        const inputRemoteShootAngle = remoteContainer.querySelector("#input-remote-angle");
        const buttonRemoteShoot = remoteContainer.querySelector("#button-remote-shoot");
        buttonRemoteShoot.onclick = this.debug_remoteShoot.bind(this, inputRemoteShootAngle);
        
    }

    // Header
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

    // Remote
    debug_remoteStartMove() {
        if (this.debug.selectedObjectId) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObjectId}/action/move`, {"action": "start"});
        }
    }
    debug_remoteStopMove() {
        if (this.debug.selectedObjectId) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObjectId}/action/move`, {"action": "stop"});
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObjectId}/action/turn`, {"direction": "stop"});
        }
    }
    debug_remoteStartTurnLeft() {
        if (this.debug.selectedObjectId) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObjectId}/action/turn`, {"direction": "left"});
        }
    }
    debug_remoteStartTurnRight() {
        if (this.debug.selectedObjectId) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObjectId}/action/turn`, {"direction": "right"});
        }
    }
    debug_remoteShoot(input) {
        if (this.debug.selectedObjectId) {
            let angle = 0.0;
            if (input.value) angle = input.value;
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObjectId}/action/shoot`, {"angle": angle});
        }
    }


}