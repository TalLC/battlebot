import {ActionDefinition, actions} from "./actions.js";
import GameManager from '../gameManager.js';
import Object3DFactory from "../view/object3DFactory.js";


/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action move.
    Param : message -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventwrapper(botState){
    return {'bot_id': botState.bot_id, 'coordinates': botState.shoot};
}

/*
    Fonction : Qui permet de determiner si le tir a eu lieu
    Param : message -> données reçu par le websocket
    Return : un booléen qui determine si l'action a été, et doit être animée.
*/
function actionSelector(botState){return !(botState.shoot === undefined);}

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
    const laserMesh = Object3DFactory.createLaserMesh(
        bot.teamColor,
        [bot.x, 1.5, bot.z],
        [to.x, 1.5, to.z]
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
        GameManager.v.disposeSceneObject(laserMesh);
    });
}
