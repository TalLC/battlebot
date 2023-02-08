import {ActionDefinition, actions} from "../actions.js";

/*
    Fonction : Permet de créer les paramètres nécéssaire à la réalisation de l'action rotate.
    Param : botState -> données reçu par le websocket pour le bot
    Return : la rotation autour de l'axe y 
*/
function eventwrapper(botState){return botState.rotate.ry === undefined? this.ry: botState.rotate.ry;}

/*
    Fonction : Qui permet de determiner si la rotation à eu lieu
    Param : botState -> données reçu par le websocket pour le bot
    Return : un booléen qui determine si l'action a été, et doit être animée.
*/
function actionSelector(botState){return !(botState.rotate === undefined);}

/*
    Fonction : Qui permet de rotate un bot
    Param : rotateCoordinate -> rotation autour de l'axe y du bot
    Return : N/A
*/
function action(rotateCoordinate){
    //let quat = new THREE.Quaternion(0, 0, 0, 0);
    //let quat = this.sceneObject.quaternion.clone();
    //let rot = new THREE.Euler(0, -1 * rotateCoordinate, 0);
    //let rot = this.sceneObject.rotation.clone();
    //rot.set(0, -1 * rotateCoordinate, 0);
    //quat.setFromEuler(rot);
    //this.sceneObject.quaternion.slerp(quat, 0.1);
    this.sceneObject.rotation.y = (-1 * rotateCoordinate);
    this.ry = (-1 * rotateCoordinate);
}

/**
* @param param
*/
actions.rotate = new ActionDefinition(eventwrapper, actionSelector, action);