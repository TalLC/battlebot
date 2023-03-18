
let instance;

export default function getInstance() {
    return instance;
};

export function initGameConfig(gameInfo) {
    instance = new Config(gameInfo);
};


class Config {
    constructor(gameInfo) {
        // Game information
        this.isDebug = gameInfo.isDebug;
        this.mapId = gameInfo.mapId;
        this.maxPlayers = gameInfo.maxPlayers;
    }
}
