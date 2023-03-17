import {ActionDefinition, actions} from "../actions.js";
import GameManager from '../../gameManager.js';
import Object3DFactory from "../../view/object3DFactory.js";


/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action move.
    Param : message -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventwrapper(botState){
    return {'id': botState.id, 'targets': botState.shoot};
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
    const bot = GameManager().bots[parameters.id];

    for (let target of parameters.targets) {
        if (!target.id) {
            shootTo(bot, target);
        } else {
            const targetObject = GameManager().getGameObjectFromId(target.id);
            if (targetObject) {
                shootTo(bot, targetObject.coordinates2D);
            } else {
                console.error(`L'objet ayant pour ID ${target.id} n'a pas été trouvé`);
            }
        }
    }
}

/**
* @param param
*/
actions.shoot = new ActionDefinition(eventwrapper, actionSelector, action);


function shootTo(bot, to) {
    const laserMesh = Object3DFactory.createLaserMesh(
        bot.teamColor,
        [bot.x, 1.5, bot.z],
        [to.x, 1.5, to.z]
    );

    //Add the mesh to the scene
    GameManager().v.scene.add(laserMesh);

    // Create a promise that resolves after 1 second
    const laserPromise = new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, 1000);
    });

    // Wait for the promise to resolve, then remove the mesh from the scene
    laserPromise.then(() => {
        GameManager().v.disposeSceneObject(laserMesh);
    });
}
