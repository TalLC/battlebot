let instance;

/**
 * Renvoie l'instance actuelle de la classe Config
 * @return {Object} - Instance actuelle de la classe Config
 */
export default function getInstance() {
    return instance;
}

/**
 * Initialise une instance de la classe Config avec les informations de jeu fournies
 * @param {Object} gameInfo - Informations de jeu
 * @return {Void} - N/A
 */
export function initGameConfig(gameInfo) {
    instance = new Config(gameInfo);
}

/**
 * Classe Config contenant les informations de jeu
 */
class Config {
    /**
     * Constructeur de la classe Config
     * @param {Object} gameInfo - Informations de jeu
     */
    constructor(gameInfo) {
        // Game information
        this.isDebug = gameInfo.isDebug;
        this.mapId = gameInfo.mapId;
        this.maxPlayers = gameInfo.maxPlayers;
        this.resetKey = 'c';
        this.resetCtrlKey = true;
        this.resetAltKey = false;
        this.resetShiftKey = false;
        this.debugAdminPassword = 'password';
    }
}
