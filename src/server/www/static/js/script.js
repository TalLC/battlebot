import GameManager from './gameManager.js'
import {actions} from './actions/actions.js';

let ws = new WebSocket("ws://localhost:8000/ws");
let update;
let game = GameManager;

function animate(){
    requestAnimationFrame( animate );
    if(update !== undefined){
        if(update.msg_type == 'BotUpdateMessage'){
            if(game.bots[update.bot_id] && game.bots[update.bot_id].objBot !== null){
                for(let actionDef in actions){
                    let selected = actions[actionDef].actionSelector(update);
                    if(selected){
                        let paramAction = actions[actionDef].eventwrapper(update);
                        game.bots[update.bot_id].action(actionDef,paramAction);
                    }
                } 
            }
        }
        game.v.renderer.render( game.v.scene, game.v.camera );
    }
}

animate();

ws.onmessage = async function(event)
{
    update = JSON.parse(event.data);
    if (update.msg_type == 'MapCreateMessage'){
        console.log('CreateMapWS')
        game.createMap(update);
    }
    else if (update.msg_type == 'BotCreateMessage'){
        console.log('CreateBot')
        game.createBot(update.bot_id, update.x, update.z, update.ry);
    }
    else if(update.msg_type == 'DisplayClientLoginMessage'){
        while(null in game.bots);
        //appel back
        console.log(update)
    }
    else if(update.msg_type == 'BotUpdateMessage'){
        update_html(update);
    }
};

function update_html(values){
//    console.log(values);

    for (const [key, value] of Object.entries(values)) {
        if (key === "x"){
            document.getElementById('x').innerHTML=value;
        } else if (key === "z"){
            document.getElementById('z').innerHTML=value;
        } else if (key === "ry"){
            document.getElementById('ry').innerHTML=value * 180/Math.PI;
        }
    }

}



