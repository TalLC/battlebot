/**
 * Envoie une requête REST avec les paramètres spécifiés.
 * @param {String} method - La méthode HTTP à utiliser pour la requête.
 * @param {String} endpoint - L'URL de l'API REST.
 * @param {Object} content - Le contenu de la requête à envoyer.
 * @return {Void} - Cette fonction ne renvoie pas de valeur.
 */
export default function sendRestMessage(method, endpoint, content) {
    // Les entêtes de la requête contiennent uniquement un type de contenu JSON
    const baseHeaders = new Headers();
    baseHeaders.append("Content-Type", "application/json");

    // Les options de la requête incluent les entêtes et l'option de redirection
    const requestOptions = {
        headers: baseHeaders,
        redirect: "follow"
    };

    // Configuration de la méthode HTTP et du contenu
    requestOptions.method = method;
    requestOptions.body = JSON.stringify(content);

    // Envoi de la requête
    fetch(endpoint, requestOptions)
        .then((response) => console.debug("REST Response", response.text()))
        .catch((error) => console.error(error));
}
