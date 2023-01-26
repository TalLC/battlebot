import * as THREE from 'three';


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

export function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}
