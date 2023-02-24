
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
        this.isDebug = gameInfo.is_debug;
        this.mapId = gameInfo.map_id;
        this.maxPlayers = gameInfo.max_players;
    }
}
