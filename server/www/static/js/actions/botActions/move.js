import {ActionDefinition, actions} from "../actions.js";
import * as TWEEN from 'tween';

/*
    Fonction : Permet de créer les paramètres nécessaire à la réalisation de l'action move.
    Param : botState -> données reçu par le websocket pour le bot
    Return : un dictionnaire contenant les positions en x et en z "final" du bot
*/
function eventWrapper(botState){return {x: botState.move.x === undefined? this.x: botState.move.x, z: botState.move.z === undefined? this.z: botState.move.z};}

/*
    Fonction : Qui permet de determiner si le move à eu lieu
    Param : botState -> données reçu par le websocket pour le bot
    Return : un booléen qui determine si l'action a été, et doit être animée.
*/
function actionSelector(botState){return !(botState.move === undefined);}

/*
    Fonction : Qui permet de move un bot
    Param : moveCoordinate -> dictionnaire avec les informations nécessaire au mouvement du bot en x et en z.
    Return : N/A
*/
function action(moveCoordinate){
    new TWEEN.Tween({x: this.sceneObject.position.x, z: this.sceneObject.position.z})
	.to({x: moveCoordinate.x , z: moveCoordinate.z}, 100)
	.easing(TWEEN.Easing.Linear.None)
	.onUpdate((coords) => {
        this.sceneObject.position.x = coords.x;
        this.sceneObject.position.z = coords.z;
        this.x = this.sceneObject.position.x;
        this.z = this.sceneObject.position.z;
    })
	.start()
}

/**
* @param param
*/
actions.move = new ActionDefinition(eventWrapper, actionSelector, action);
