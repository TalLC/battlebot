import logger from '../logger.js';
import BaseWsMessage from './baseWsMessage.js'
import GameManager from '../gameManager.js';
import BotManager from '../botManager.js';
import sendRestMessage from '../utils/rest.js'
import GameConfig from '../config.js';


export default class DisplayClientLoginMessage extends BaseWsMessage {
    constructor(message){
        super();
        this.loginId = message.login_id
    }

    exec() {
        GameManager().loginId = this.loginId;
        
        // On reçoit la création des bots avant le login du client display
        logger.debug('Waiting for bots to be created');
        
        this.waitUntilBotsInitialized()
        .then(function(botsCount) {
            // Les bots sont créés, on démarre la partie dans le Back
            if (GameConfig().isDebug) {
                logger.debug(`${botsCount} bots created!`);
                logger.debug('Start game');
            } 

            // Affichage du jeu
            GameManager().start();

            // Démarrage du jeu côté Back
            sendRestMessage('PATCH', '/display/clients/action/ready', { login_id: GameManager().loginId });
        });

    }

    waitUntilBotsInitialized() {
        return new Promise(function(resolve, reject) {
            const intervalId = setInterval(function() {
                // On est prêt lorsque tous les bots attendus sont créés
                const botsCount = Object.keys(BotManager.bots).length;
                if (botsCount >= GameConfig().maxPlayers) {
                    clearInterval(intervalId);
                    resolve(botsCount);
                }
            }, 100);
        });
    }
}
