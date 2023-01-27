import sendRestMessage from './rest.js'


export default class DebugUi {

    constructor(debug) {
        this.debug = debug;

        // Header
        const headerContainer = document.getElementById("header-container");

        const buttonForceStart = headerContainer.querySelector("#header-button-force-start");
        buttonForceStart.onclick = this.forceStartGame.bind(this);
        
        const buttonAddBot = headerContainer.querySelector("#header-button-add-bot");
        buttonAddBot.onclick = this.addBot.bind(this);
        
        const buttonKillBot = headerContainer.querySelector("#header-button-kill-bot");
        buttonKillBot.onclick = this.killBot.bind(this);

        // Remote
        this.remoteContainer = document.getElementById("remote-container");
        
        const buttonRemoteStartMove = this.remoteContainer.querySelector("#button-remote-up");
        buttonRemoteStartMove.onclick = this.remoteStartMove.bind(this);
        
        const buttonRemoteStopMove = this.remoteContainer.querySelector("#button-remote-stop");
        buttonRemoteStopMove.onclick = this.remoteStopMove.bind(this);
        
        const buttonRemoteStartTurnLeft = this.remoteContainer.querySelector("#button-remote-left");
        buttonRemoteStartTurnLeft.onclick = this.remoteStartTurnLeft.bind(this);
        
        const buttonRemoteStartTurnRight = this.remoteContainer.querySelector("#button-remote-right");
        buttonRemoteStartTurnRight.onclick = this.remoteStartTurnRight.bind(this);
        
        const inputRemoteShootAngle = this.remoteContainer.querySelector("#input-remote-angle");
        const buttonRemoteShoot = this.remoteContainer.querySelector("#button-remote-shoot");
        buttonRemoteShoot.onclick = this.remoteShoot.bind(this, inputRemoteShootAngle);

        const buttonRemoteKill = this.remoteContainer.querySelector("#button-remote-kill");
        buttonRemoteKill.onclick = this.remoteKill.bind(this);
    }

    setRemoteHidden(state) {
        this.remoteContainer.hidden = state;
    }

    // Header
    forceStartGame() {
        sendRestMessage('PATCH', '/game/action/start', {"api_password": "password"});
    }

    addBot() {
        sendRestMessage('PATCH', '/bots/action/add', {"api_password": "password"});
    }

    killBot() {
        let botId = prompt("ID du bot :", "0-0-0-0-0");
        if (botId !== null && botId !== "") {
            sendRestMessage('PATCH', `/bots/${botId}/action/kill`, {"api_password": "password"});
        }
    }

    // Remote mouvements
    remoteStartMove() {
        if (this.debug.selectedObject.id) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/move`, {"action": "start"});
        }
    }
    remoteStopMove() {
        if (this.debug.selectedObject.id) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/move`, {"action": "stop"});
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/turn`, {"direction": "stop"});
        }
    }
    remoteStartTurnLeft() {
        if (this.debug.selectedObject.id) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/turn`, {"direction": "left"});
        }
    }
    remoteStartTurnRight() {
        if (this.debug.selectedObject.id) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/turn`, {"direction": "right"});
        }
    }

    // Remote actions
    remoteShoot(input) {
        if (this.debug.selectedObject.id) {
            let angle = 0.0;
            if (input.value) angle = input.value;
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/shoot`, {"angle": angle});
        }
    }

    remoteKill() {
        if (this.debug.selectedObject.id) {
            sendRestMessage('PATCH', `/bots/${this.debug.selectedObject.id}/action/kill`, {"api_password": "password"});
        }
    }

}