import {ActionDefinition, actions} from "./actions.js";
import GameManager from '../gameManager.js';
import * as THREE from 'three';


/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action move.
    Param : message -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventwrapper(message){
    return {
        bot_id: message.bot_id,
        x: message.coordinates.x,
        z: message.coordinates.z
    };
}

/*
    Fonction : Qui permet de determiner si le tir a eu lieu
    Param : message -> données reçu par le websocket
    Return : un booléen qui determine si l'action a été, et doit être animée.
*/
function actionSelector(message){
    return message.msg_type && message.msg_type === "BotShootAtCoordinates";
}

/*
    Fonction : Qui affiche le tir du bot
    Param : parameters -> dictionnaire avec les informations nécéssaire à l'action.
    Return : N/A
*/
function action(parameters){

    const bot = GameManager.bots[parameters.bot_id];

    const laserMesh = createLaserMesh(
        bot.teamColor,
        new THREE.Vector3(bot.x, 1.5, bot.z),
        new THREE.Vector3(0.0, 1.5, 0.0)
    );

    //Add the mesh to the scene
    GameManager.v.scene.add(laserMesh);

    // Create a promise that resolves after 2 seconds
    const laserPromise = new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, 2000);
    });

    // Wait for the promise to resolve, then remove the mesh from the scene
    laserPromise.then(() => {

        if (!(laserMesh instanceof THREE.Object3D)) return false;

        // for better memory management and performance
        if (laserMesh.geometry) laserMesh.geometry.dispose();

        if (laserMesh.material) {
            if (laserMesh.material instanceof Array) {
                // for better memory management and performance
                laserMesh.material.forEach(material => material.dispose());
            } else {
                // for better memory management and performance
                laserMesh.material.dispose();
            }
        }
        laserMesh.removeFromParent(); // the parent might be the scene or another Object3D, but it is sure to be removed this way
    });
    
}

/**
* @param param
*/
actions.shoot = new ActionDefinition(eventwrapper, actionSelector, action);


function createLaserMesh(color, from, to) {
        // Create a material
        let lineMaterial = new THREE.MeshBasicMaterial({
            color: color
        });
    
        // Create a path for the tube
        let path = new THREE.CatmullRomCurve3( [
            from, to
        ] );
    
        // Create the tube geometry
        let tubeGeometry = new THREE.TubeGeometry(
            path,
            100,
            0.15,
            8,
            true
        );
    
        // Create the tube mesh
        return new THREE.Mesh(tubeGeometry, lineMaterial);
}

