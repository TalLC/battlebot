import {ActionDefinition, actions} from "./actions.js";
import GameManager from '../gameManager.js';
import * as THREE from 'three';


/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action move.
    Param : message -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventwrapper(message){
    return message;
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

    for (let coordinates of parameters.coordinates) {
        shootTo(bot, coordinates);
    }
}

/**
* @param param
*/
actions.shoot = new ActionDefinition(eventwrapper, actionSelector, action);


function shootTo(bot, to) {
    console.log(to);
    const laserMesh = createLaserMesh(
        bot.teamColor,
        new THREE.Vector3(bot.x, 1.5, bot.z),
        new THREE.Vector3(to.x, 1.5, to.z)
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
        GameManager.v.disposeObject3D(laserMesh);
    });
}

function createLaserMesh(color, start, end) {
    // Create a material
    let lineMaterial = new THREE.MeshBasicMaterial({
      color: color
    });
  
    //calculate the distance between start and end point
    let distance = start.distanceTo(end);
    
    //calculate the number of segments needed
    const desired_detail_level = 2;
    let segments = Math.ceil(distance / desired_detail_level);
    
    // Create a path for the tube
    let path = new THREE.CatmullRomCurve3([start, end]);
    
    // Create the tube geometry
    let tubeGeometry = new THREE.TubeGeometry(
      path,
      segments,
      0.15,
      8,
      true
    );
  
    // Create the tube mesh
    return new THREE.Mesh(tubeGeometry, lineMaterial);
}
