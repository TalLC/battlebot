import BaseWsMessage from './baseWsMessage.js'
import { initGameManager } from '../gameManager.js';
import { initGameConfig } from '../config.js';
import GameManager from '../gameManager.js';


export default class GameInfoMessage extends BaseWsMessage {
    constructor(message){
        super();
        this.gameInfo = {
            isDebug: message.is_debug,
            mapId: message.map_id,
            maxPlayers: message.max_players
        };
    }

    exec() {
        // Création de la config du jeu
        initGameConfig(this.gameInfo);

        // On a besoin de la config du jeu pour déclarer le GameManager
        initGameManager();

        // Déclenchement de la boucle d'update du visuel ThreeJs
        GameManager().viewController.animate();
    }
}
