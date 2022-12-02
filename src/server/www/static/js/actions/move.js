import {ActionDefinition, actions} from "./actions.js";
import * as THREE from '../view/three.module.js';

/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action move.
    Param : botState -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventwrapper(botState){return {x: botState.x === undefined? this.x: botState.x, z: botState.x === undefined? this.z: botState.z};}

/*
    Fonction : Qui permet de determiner si le move à eu lieu
    Param : botState -> données reçu par le websocket pour le bot
    Return : un booléen qui determine si l'action a été, et doit être animée.
*/
function actionSelector(botState){return botState.x || botState.z;}

/*
    Fonction : Qui permet de move un bot
    Param : moveCoordinate -> dictionnaire avec les informations nécéssaire au mouvement du bot en x et en z.
    Return : N/A
*/
function action(moveCoordinate){
    //let posDest = new THREE.Vector3(moveCoordinate.x, 0.5, moveCoordinate.z);
    let posDest = this.objBot.position.clone();
    posDest.set(moveCoordinate.x, 0.5, moveCoordinate.z);
    this.objBot.position.lerp(posDest, 0.1);
    this.x = posDest.x;
    this.z = posDest.z;
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventwrapper, actionSelector, action);
