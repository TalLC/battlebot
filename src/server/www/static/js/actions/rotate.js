import {ActionDefinition, actions} from "./actions.js";

function eventwrapper(botState){return botState.ry === undefined? this.ry: botState.ry;}

function actionSelector(botState){return !(botState.ry === undefined);}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function action(rotate_coordinate){
    console.log(rotate_coordinate);
    //let rotInit = this.ry;
    //let rotDest = rotate_coordinate;
    //let rotIndex = (rotInit - rotDest) / 10
    //for(let i = 0; i < 10; i += 1){
    //this.objBot.rotateY(rotIndex);
    //    await sleep(5)
    //}
    this.objBot.rotation.y = -1 * rotate_coordinate;
    this.ry = rotate_coordinate;
}

/**
* @param param
*/
actions.rotate = new ActionDefinition(eventwrapper, actionSelector, action);
