
let instance;

export class Logger {
    constructor() {
        if (!instance) {
            instance = this;
            this.isDebug = true;
        }
        return instance;
    }

    /**
     * Affiche un message de débogage dans la console si le mode débogage est activé.
     * @param {string} msg - Le message à afficher.
     */
    debug(msg) {
        if (this.isDebug) console.log(msg);
    }
}

export default new Logger();
