import GameManager from "../gameManager.js";
import sendRestMessage from "../utils/rest.js";

export default class DebugUi {
    constructor(debug) {
        this.debug = debug;

        // Startgame
        const startGameContainer = document.getElementById("startgame-container");
        const buttonAddBot = startGameContainer.querySelector("#debug-button-add-bot");
        buttonAddBot.hidden = false;
        buttonAddBot.onclick = this.addBot.bind(this);

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

    /**
     * Masque ou affiche le container pour les actions à distance
     * @param {Boolean} state - Masquer ou afficher le container
     */
    setRemoteHidden(state) {
        this.remoteContainer.hidden = state;
    }

    // Header
    /**
     * Ajoute un bot
     */
    addBot() {
        sendRestMessage("PATCH", "/bots/action/add", {
            api_password: "password"
        });
    }

    /**
     * Tue un bot spécifié par l'utilisateur
     */
    killBot() {
        let botId = prompt("ID du bot :", "0-0-0-0-0");
        if (botId !== null && botId !== "") {
            sendRestMessage("PATCH", `/bots/${botId}/action/kill`, {
                api_password: "password"
            });
        }
    }

    /**
     * Active ou désactive l'affichage des collisions pour tous les GameObjects
     */
    toggleCollisions() {
        for (const obj of Object.values(GameManager().allGameObjects)) {
            obj.toggleCollisions();
        }
    }

    // Remote mouvements
    /**
     * Commence le mouvement du bot sélectionné vers l'avant
     */
    remoteStartMove() {
        if (this.debug.selectedObject.id) {
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/move`, { action: "start" });
        }
    }
    /**
     * Arrête le mouvement et la rotation du bot sélectionné.
     */
    remoteStopMove() {
        if (this.debug.selectedObject.id) {
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/move`, { action: "stop" });
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/turn`, { direction: "stop" });
        }
    }

    /**
     * Démarre la rotation du bot sélectionné vers la gauche.
     */
    remoteStartTurnLeft() {
        if (this.debug.selectedObject.id) {
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/turn`, { direction: "left" });
        }
    }

    /**
     * Démarre la rotation du bot sélectionné vers la droite.
     */
    remoteStartTurnRight() {
        if (this.debug.selectedObject.id) {
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/turn`, { direction: "right" });
        }
    }

    /**
     * Effectue un tir du bot sélectionné avec l'angle spécifié.
     * @param {HTMLInputElement} input - L'input contenant l'angle du tir.
     */
    remoteShoot(input) {
        if (this.debug.selectedObject.id) {
            let angle = 0.0;
            if (input.value) angle = input.value;
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/shoot`, { angle: angle });
        }
    }

    /**
     * Tue le bot sélectionné.
     */
    remoteKill() {
        if (this.debug.selectedObject.id) {
            sendRestMessage("PATCH", `/bots/${this.debug.selectedObject.id}/action/kill`, { api_password: "password" });
        }
    }
}
