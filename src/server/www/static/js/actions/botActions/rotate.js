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
    const targetRotation = rotateCoordinate % (Math.PI * 2);
    const tween = new TWEEN.Tween({rotation: this.sceneObject.rotation.y})
	.to({rotation: targetRotation}, 100)
	.easing(TWEEN.Easing.Quadratic.InOut)
	.onUpdate((coords) => {
        console.log(coords.rotation);
        this.sceneObject.rotation.y = coords.rotation;
    })
	.start()
}

/**
* @param param
*/
actions.rotate = new ActionDefinition(eventwrapper, actionSelector, action);
