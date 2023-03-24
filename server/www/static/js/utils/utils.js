import * as THREE from "three";

/**
 * Convertit une chaîne de caractères représentant une couleur en un objet THREE.Color.
 * @param {String} strColor - La chaîne de caractères représentant la couleur, en format décimal ou hexadécimal.
 * @returns {THREE.Color} - Un objet THREE.Color représentant la couleur.
 */
export function colorStrToNumber(strColor) {
    // Default color
    let numberColor = new THREE.Color(0xffffff);

    try {
        // Parsing string color
        numberColor = new THREE.Color(Number(strColor));
    } catch (error) {
        console.error(`Could not cast "${strColor}" into a number`);
    }

    return numberColor;
}

/**
 * Retourne un nombre entier aléatoire entre 0 et le nombre maximum spécifié (exclus).
 * @param {Number} max - Le nombre maximum pour la génération du nombre aléatoire (exclus).
 * @returns {Number} - Un nombre entier aléatoire entre 0 et le nombre maximum spécifié (exclus).
 */
export function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}
