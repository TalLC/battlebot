import GameManager from '../gameManager.js';
import sendRestMessage from '../utils/rest.js'


export default class DebugUi {

    constructor(debug) {
        this.debug = debug;

        // Startgame
        const startGameContainer = document.getElementById("startgame-container");
        const buttonAddBot = startGameContainer.querySelector("#header-button-add-bot");
        buttonAddBot.onclick = this.addBot.bind(this);
        
        // Scroll text
        const scrollText = document.getElementById("startgame-scroll-text");
        fetch('https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/g_game.c')
            .then((response) => response.text())
            .then((data) => {
                scrollText.innerHTML = data;
                scrollText.style.height = scrollText.scrollHeight;
            });

        // Debug info
        const headerContainer = document.getElementById("info-container-buttons");

        const buttonKillBot = headerContainer.querySelector("#button-kill-bot");
        buttonKillBot.onclick = this.killBot.bind(this);
        
        const buttonToggleCollisions = headerContainer.querySelector("#button-collisions");
        buttonToggleCollisions.onclick = this.toggleCollisions.bind(this);
        
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
    addBot() {
        sendRestMessage('PATCH', '/bots/action/add', {"api_password": "password"});
    }

    killBot() {
        let botId = prompt("ID du bot :", "0-0-0-0-0");
        if (botId !== null && botId !== "") {
            sendRestMessage('PATCH', `/bots/${botId}/action/kill`, {"api_password": "password"});
        }
    }

    toggleCollisions() {
        for(const obj of Object.values(GameManager.bots)) {
            obj.toggleCollisions();
        }
        for(const obj of Object.values(GameManager.mapObjects)) {
            obj.toggleCollisions();
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