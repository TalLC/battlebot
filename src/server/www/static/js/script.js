import GameManager from './gameManager.js';
import {actions} from './actions/actions.js';

let ws = new WebSocket("ws://localhost:8000/ws");
let game = GameManager;
let update = [];

/*
    Fonction : Permet la réalistion des actions pour un des bots, reçu dans un appel websocket.
    Param : message -> correspont aux données pour un bot, reçu dans un appel websocket.
    Return : N/A

function doAction(message){
    if(message.msg_type === 'BotUpdateMessage'){
        if(game.bots[message.bot_id] && game.bots[message.bot_id].objBot !== null){
            // return la promise des actions du bot
            for(let actionDef in actions){
                let selected = actions[actionDef].actionSelector(message);
                if(selected){
                    let paramAction = actions[actionDef].eventwrapper(message);
                    game.bots[message.bot_id].action(actionDef,paramAction);
                }
            }
        }
    }
}
*/
/*
    Fonction : Permet une animation fluide à chaque frame.
    Param : N/A
    Return : N/A

function animate(){
    requestAnimationFrame( animate );
    if(update[0] !== undefined && update[0].messages !== undefined){
        for(let i = 0; i < update[0].messages.length; i++){
            //ajouter toute les promises à un tableau
            doAction(update[0].messages[i]);
        }
        //promise.all ???
        game.v.renderer.render( game.v.scene, game.v.camera );
        update.shift();
    }
    else
        game.v.renderer.render( game.v.scene, game.v.camera );
}
*/
/*
    Fonction : Permet la réalistion des actions pour un des bots, reçu dans un appel websocket.
    Param : message -> correspont aux données pour un bot, reçu dans un appel websocket.
    Return : N/A
*/
function doAction(message){
    let promise = Promise.resolve();
    if(game.bots[message.bot_id] && game.bots[message.bot_id].objBot){
        for(let actionDef in actions){
            let selected = actions[actionDef].actionSelector(message);
            if(selected){
                let paramAction = actions[actionDef].eventwrapper(message);
                promise = promise.then(() => {
                    game.bots[message.bot_id].action(actionDef,paramAction);
                });
            }
        }
    }
    return promise.then(() => {
        requestAnimationFrame( animate );
        game.v.renderer.render( game.v.scene, game.v.camera );
    });
}

/*
Fonction : Permet une animation fluide à chaque frame.
Param : N/A
Return : N/A
*/
function animate(){
if(update[0] !== undefined && update[0].messages !== undefined){
    let promises = [];
    for(let i = 0; i < update[0].messages.length; i++){
        //ajouter toute les promises à un tableau
        promises.push(doAction(update[0].messages[i]));
    }
    Promise.all(promises).then(() =>{
        //game.v.renderer.render( game.v.scene, game.v.camera );
    });
    update.shift();
}
else{
    requestAnimationFrame( animate );
    game.v.renderer.render( game.v.scene, game.v.camera );
}
}

animate();

/*
    Fonction : Permet la récupération en continue des données reçues via websocket
    Param : event -> Correspont au donnée de chaque appel websocket
    Return : N/A
*/
ws.onmessage = async function(event)
{
    console.log(event.data);
    update.push(JSON.parse(event.data));
    console.log(update);
    if (update[0].msg_type == 'MapCreateMessage'){
        console.log('CreateMapWS');
        game.createMap(update[0]);
        update.shift();
    }
    else if (update[0].msg_type == 'BotCreateMessage'){
        console.log('CreateBot');
        game.createBot(update[0].bot_id, update[0].x, update[0].z, update[0].ry);
        update.shift();
    }
    else if(update[0].msg_type == 'DisplayClientLoginMessage'){
        while(null in game.bots);
        //appel back
        console.log(update[0]);
        update.shift();
    }
};
