/*
 Classe permettant de gérer la configuration de l'application front.
*/

class Config {
    constructor(){
        this.debugMode = true;
    }

    isDebug() {
        return this.debugMode;
    }
}

export default new Config();
