import logger from "../logger.js";
import * as TWEEN from "tween";
import { updateMessageQueue } from "../messages/messageHandler.js";
import GameManager from "../gameManager.js";

/**
 * La classe Animator est un singleton qui gère la mise à jour du rendu threeJs et des animations.
 */
let instance;

export default class Animator {
    /**
     * Construit l'instance Animator si elle n'existe pas déjà et démarre la boucle d'animation.
     */
    constructor() {
        if (!instance) {
            instance = this;

            // Limitation du framerate
            this.targetFPS = 60; // Nombre de FPS ciblé
            this.targetDeltaTime = 1000 / this.targetFPS;
            this.lastFrameTime = null;

            // On lie l'instance courante à cette fonction car elle fait des appels récursifs
            this.animate = this.animate.bind(this);
            this.animate();
        }

        return instance;
    }

    /**
     * La fonction animate gère l'affichage de la scène.
     * Elle traite les messages de la file d'attente updateMessageQueue et exécute les actions en conséquence.
     * Met à jour les animations et rend la scène du gameManager.
     */
    animate() {
        const currentTime = performance.now();

        if (this.lastFrameTime === null) {
            this.lastFrameTime = currentTime;
        }

        const deltaTime = currentTime - this.lastFrameTime;
        if (deltaTime >= this.targetDeltaTime) {
            if (updateMessageQueue[0] !== undefined && updateMessageQueue[0].messages !== undefined) {
                let promesses = [];

                for (let i = 0; i < updateMessageQueue[0].messages.length; i++) {
                    promesses.push(GameManager().doAction(updateMessageQueue[0].messages[i]));
                }
                Promise.all(promesses).then(() => {
                    window.requestAnimationFrame(this.animate);
                    TWEEN.update();
                    GameManager().render();
                });
                updateMessageQueue.shift();
            } else {
                window.requestAnimationFrame(this.animate);
                TWEEN.update();
                GameManager().render();
            }

            this.lastFrameTime = currentTime;
        } else {
            window.requestAnimationFrame(this.animate);
        }
    }


}
