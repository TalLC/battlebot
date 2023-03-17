import {ActionDefinition, actions} from "../actions.js";
import TWEEN from 'tween';

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
    this.sceneObject.rotation.y = -1 * rotateCoordinate;
    this.ry = -1 * rotateCoordinate;
}

/*
    Fonction : Qui permet de rotate un bot avec TWEEN
    Param : rotateCoordinate -> rotation autour de l'axe y du bot
    Return : N/A

function action(rotateCoordinate){
    const targetRotation = -1 * rotateCoordinate;
    console.log("ry " + this.ry + " new " + targetRotation);
    if(Math.abs(targetRotation - this.ry) < 1){
        this.ry = targetRotation;
        const tween = new TWEEN.Tween({rotation: this.sceneObject.rotation.y})
	    .to({rotation: targetRotation}, 100)
	    .easing(TWEEN.Easing.Linear.None)
    	.onUpdate((coords) => {
            this.sceneObject.rotation.y = coords.rotation;
        })
	    .start()
    }
    else if (targetRotation > -0.5){
        this.ry = targetRotation;
        const tween = new TWEEN.Tween({rotation: this.sceneObject.rotation.y})
	    .to({rotation: Math.PI * 2 * -1}, 100)
	    .easing(TWEEN.Easing.Linear.None)
    	.onUpdate((coords) => {
            this.sceneObject.rotation.y = coords.rotation;
        })
	    .start()
        .onComplete(() => {
            this.sceneObject.rotation.y = 0;
            const last = new TWEEN.Tween({rotation: this.sceneObject.rotation.y})
            .to({rotation: targetRotation}, 100)
            .easing(TWEEN.Easing.Linear.None)
            .onUpdate((coords) => {
                this.sceneObject.rotation.y = coords.rotation;
            })
            .start()})
    }
    else{
        this.ry = targetRotation;
        const tween = new TWEEN.Tween({rotation: this.sceneObject.rotation.y})
	    .to({rotation: 0}, 100)
	    .easing(TWEEN.Easing.Linear.None)
    	.onUpdate((coords) => {
            this.sceneObject.rotation.y = coords.rotation;
        })
	    .start()
        .onComplete(() => {
            this.sceneObject.rotation.y = Math.PI * 2 * -1;
            const last = new TWEEN.Tween({rotation: this.sceneObject.rotation.y})
            .to({rotation: targetRotation}, 100)
            .easing(TWEEN.Easing.Linear.None)
            .onUpdate((coords) => {
                this.sceneObject.rotation.y = coords.rotation;
            })
            .start()})
    }
}
*/
/**
* @param param
*/
actions.rotate = new ActionDefinition(eventwrapper, actionSelector, action);
