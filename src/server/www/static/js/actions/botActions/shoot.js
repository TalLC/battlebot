import {ActionDefinition, actions} from "../actions.js";
import GameManager from '../../gameManager.js';
import TWEEN from 'tween';
import object3DFactory from "../../view/object3DFactory.js";

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
            GameManager().addBullet(bot).then(bullet => {
                console.log(bullet);
                const tween = new TWEEN.Tween({x: bullet.position.x , z: bullet.position.z})
                .to({x: target.x , z: target.z}, 10000)
                .easing(TWEEN.Easing.Linear.None)
                .onUpdate((coords) => {
                    bullet.position.x = coords.x;
                    bullet.position.z = coords.z;
                    if (bullet.position.x === target.x && bullet.position.z === target.z){
                        GameManager().removeBullet(bullet);
                    }
                })
                .start()
            });

        } else {
            const targetObject = GameManager().getGameObjectFromId(target.id);
            if (targetObject) {
                GameManager().addBullet(bot).then(bullet => {
                    console.log(GameManager.bots[bot.id].bullet);
                    const tween = new TWEEN.Tween({x: bullet.position.x , z: bullet.position.z})
                    .to({x: targetObject.coordinates2D.x , z: targetObject.coordinates2D.z}, 10000)
                    .easing(TWEEN.Easing.Linear.None)
                    .onUpdate((coords) => {
                        bullet.position.x = coords.x;
                        bullet.position.z = coords.z;
                        if (bullet.position.x === targetObject.coordinates2D.x && bullet.position.z === targetObject.coordinates2D.z){
                            GameManager().removeBullet(bullet);
                        }
                    })
                    .start()
                });
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
