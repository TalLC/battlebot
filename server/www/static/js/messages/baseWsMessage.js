/**
 * Classe abstraite représentant un message WebSocket de base.
 */
export default class BaseWsMessage {
    /**
     * Constructeur de la classe.
     * @param {Object} message - Message WebSocket.
     */
    constructor(message) {}

    /**
     * Fonction exécutant le traitement du message.
     * Cette fonction doit être implémentée dans les classes enfants.
     */
    exec() {}
}
