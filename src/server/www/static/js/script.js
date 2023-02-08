import GameManager from './gameManager.js';
import {actions} from './actions/actions.js';
import * as TWEEN from 'tween';
import sendRestMessage from './utils/rest.js'


let ws = new WebSocket(`ws://${window.location.host}/ws`);
let game = GameManager;
let update = [];


/*
    Fonction : Permet la réalistion des actions pour un des bots, reçu dans un appel websocket.
    Param : message -> correspond aux données pour un bot, reçu dans un appel websocket.
    Return : N/A
*/
function doAction(message){
    // Création d'une promise vide
    let promise = Promise.resolve();
    //console.log(message.msg_type);
    if (message.msg_type === "BotUpdateMessage") {
        // On vérifie si le bot existe
        if(game.bots[message.id] && game.bots[message.id].sceneObject){
            
            // Parcours des actions enregistrées
            for(let actionDef in actions){

                // Choix de l'action à effectuer suivant les arguments trouvés dans le message
                let selected = actions[actionDef].actionSelector(message);
                
                if(selected){
                    let paramAction = actions[actionDef].eventwrapper(message);
                    promise = promise.then(() => {
                        game.bots[message.id].action(actionDef,paramAction);
                    });
                }
            }
        }
    } else {
        for(let actionDef in actions){

            // Choix de l'action à effectuer suivant les arguments trouvés dans le message
            let selected = actions[actionDef].actionSelector(message);

            if(selected){
                let paramAction = actions[actionDef].eventwrapper(message);
                promise = promise.then(() => {
                    game.action(actionDef,paramAction);
                });
            }
        }
    }

    return promise;
}

/*
    Fonction : Permet l'affichage de la scene.
    Param : N/A
    Return : N/A
*/
function animate(){
    if(update[0] !== undefined && update[0].messages !== undefined){
        let promises = [];
        // console.log(update[0].messages)
        for(let i = 0; i < update[0].messages.length; i++){
            promises.push(doAction(update[0].messages[i]));
        }
        Promise.all(promises).then(() =>{
            requestAnimationFrame( animate );
            TWEEN.update();
            game.render();
        });
        update.shift();
    }
    else{
        requestAnimationFrame( animate );
        TWEEN.update()
        game.render();
    }
}

animate();

/*
    Fonction : Permet la récupération en continue des données reçues via websocket
    Param : event -> Correspont au donnée de chaque appel websocket
    Return : N/A
*/
ws.onmessage = async function(event) {
    const message = JSON.parse(event.data);
    // Messages d'update multiples
    if (message.messages !== undefined) {
        update.push(message);
    }
    // Messages seuls
    else {
        if (message.msg_type == 'MapCreateMessage'){
            console.log('CreateMapWS');
            game.createMap(message);
        }
        else if (message.msg_type == 'BotCreateMessage'){
            console.log('CreateBot');
            game.addBot(message);
        }
        else if (message.msg_type == 'DisplayClientLoginMessage'){
            game.loginId = message.login_id;
            while(null in game.bots);
            console.log('Start game');
            game.start();
            sendRestMessage('PATCH', '/display/clients/action/ready', {login_id: game.loginId});
        }
    }
};
