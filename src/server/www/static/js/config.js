

class Config {
    constructor(){
        this.debugMode = false;
    }

    isDebug() {
        return this.debugMode;
    }
}

export default new Config();
