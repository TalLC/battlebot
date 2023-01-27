import {ActionDefinition, actions} from "./actions.js";

/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action move.
    Param : botState -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventwrapper(botState){return {x: botState.move.x === undefined? this.x: botState.move.x, z: botState.move.z === undefined? this.z: botState.move.z};}

/*
    Fonction : Qui permet de determiner si le move à eu lieu
    Param : botState -> données reçu par le websocket pour le bot
    Return : un booléen qui determine si l'action a été, et doit être animée.
*/
function actionSelector(botState){return !(botState.move === undefined);}

/*
    Fonction : Qui permet de move un bot
    Param : moveCoordinate -> dictionnaire avec les informations nécéssaire au mouvement du bot en x et en z.
    Return : N/A
*/
function action(moveCoordinate){
    //let posDest = new THREE.Vector3(moveCoordinate.x, 0.5, moveCoordinate.z);
    //let posDest = this.sceneObject.position.clone();
    //posDest.set(moveCoordinate.x, 0.5, moveCoordinate.z);
    //this.sceneObject.position.lerp(posDest, 0.1);
    this.sceneObject.position.x = moveCoordinate.x;
    this.sceneObject.position.z = moveCoordinate.z;
    this.x = moveCoordinate.x;
    this.z = moveCoordinate.z;
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventwrapper, actionSelector, action);
