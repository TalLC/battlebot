import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'three/examples/jsm/libs/stats.module';
import bot from './bot.js'
import View3DController from './view/view3DController.js'
import GameManager from './gameManager.js'
import {actions} from './actions/actions.js';
import { CubeRefractionMapping, SkeletonHelper } from './view/three.module.js';


//Websocket

let ws = new WebSocket("ws://localhost:8000/ws");
var bot_obj = {};
var obj_list = {
    'tree_small':'tree_small.glb',
    'wall_plain':'wall_plain.glb',
    'ground':'ground.glb',
    'water':'water.glb'
};
var map_list = [];


function update_map(update){
    if (map_list[update.x][update.z])
    {
        delete(update.tile_object)
        create_object(update.tile_object, update.x * 2, 1, update.z * 2)
    }
    else
    {
        console.log(update)
        create_object(update.tile, update.x * 2, 0, update.z * 2)
        if (update.tile_object != air)
            create_object(update.tile_object, update.x * 2, 1, update.z * 2)
    }
};

function create_map(map_data){
    for (var h = 0; h < map_data.height; h++)
    {
        var current_line = [];
        for (var w = 0; w < map_data.width; w++)
        {
            for (var tile in map_data['tiles'])
            {
                tile = map_data['tiles'][tile]
                if (h == tile['x'] && w == tile['z'])
                    current_line.push({'tile': create_object(tile['tile'], h * 2, 0, w * 2), 'object': create_object(tile['tile_object'], h * 2, 1, w * 2)});
            };
        };
        map_list.push(current_line);
    };
}

ws.onmessage = async function(event)
{
    let update = JSON.parse(event.data);
    if (update.msg_type == 'BotCreateMessage'){
        let botState = update;
        await game.createBot(botState.id, botState.x, botState.z, botState.ry);
    }
    else if (update.msg_type == 'BotUpdateMessage'){
        let botState = update;
        for(actionDef in actions){
            let selected = actions[actionDef].actionSelector(botState);
            if(selected){
                let paramAction = actions[actionDef].eventwrapper(botState);
                game.bots[botState.id].action(actionDef,paramAction);
            }
        }
    }
    else if (update.msg_type == 'MapUpdateMessage'){
        update_map(update)
    }
    //else if (update.msg_type == 'MapCreateMessage'){
    //    create_map(update)
    //    console.log(map_list)
    //}
};

let game = GameManager;

function animate(){
    requestAnimationFrame( animate );
    game.v.renderer.render( game.v.scene, game.v.camera );

}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
 }

async function creation(){
    await game.createBot('985984', 0, 0, 0);
    let test = game.bots['985984'];
    console.log("im ready");
    console.log(test);
    await test.action('move', {x:0.1, z:0.1});
    console.log(test);
}

animate();
creation();


