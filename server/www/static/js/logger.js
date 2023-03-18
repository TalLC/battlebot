
let instance;

export class Logger {
    constructor() {
        if (!instance) {
            instance = this;
            this.isDebug = true;
        }
        return instance;
    }

    debug(msg) {
        if (this.isDebug) console.log(msg);
    }
}

export default new Logger();
