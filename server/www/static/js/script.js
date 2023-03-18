import MessageHandler from "./messages/messageHandler.js";

let ws = new WebSocket(`ws://${window.location.host}/ws`);
let messageHandler = new MessageHandler();

/**
 * Fonction de gestion de message pour WebSocket qui analyse et gère les messages entrants.
 * @param {Object} event - L'événement de message WebSocket contenant les données du message.
 * @return {Promise<void>} - Une promesse qui se résout une fois que le message a été traité.
 */
ws.onmessage = async function (event) {
    messageHandler.handle(JSON.parse(event.data));
};
