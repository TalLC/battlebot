import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'three/examples/jsm/libs/stats.module';
import bot from './bot.js'
import View3DController from './view/view3DController.js'


//Websocket

let ws = new WebSocket("ws://localhost:8000/ws");
var bot_obj = {};
var obj_list = {
    'tree_small':'tree_small.glb',
    'wall_plain':'wall_plain.glb',
    'ground':'ground.glb',
    'water':'water.glb'
};
const EnumStatus = 
{
    NONE : 0,
    HIT : 1,
    SHOOTING : 2,
    SHIELD_SHOW : 4,
    SHIELD_HIDE : 8
}
var map_list = [];

// Scene
const scene = new THREE.Scene()

// Caméra
// const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 1000 );

let width = window.innerWidth;
let height = window.innerHeight;

const camera = new THREE.OrthographicCamera( width / - 50, width / 50, height / 50, height / - 50, -10000, 100000 );
camera.position.set(2, 2, 2);
camera.lookAt(0, 0, 0);


// Render
const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

// Controls
const controls = new OrbitControls( camera, renderer.domElement );
controls.update();

// Light
const light = new THREE.AmbientLight( 0xffffff , 1.5); // soft white light
scene.add( light );

const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
directionalLight.position.x = -10;
directionalLight.position.z = -10;
scene.add( directionalLight );

function create_object(name, x, y, z){

}

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

ws.onmessage = function(event)
{
    let update = JSON.parse(event.data);
    console.log(update)
    if (update.msg_type == 'BotCreateMessage'){
        bot_list[update.id] = new bot(update)
    }
    else if (update.msg_type == 'BotUpdateMessage'){
        botState = update
        for(actionDef in actions){
            let selected = actionDef.actionSelector(botState);
            if(selected){
                let paramAction = actionDef.eventwrapper(botState);
                bot.action(actionKey,paramAction);
            }
        }
    }
    else if (update.msg_type == 'MapUpdateMessage'){
        update_map(update)
    }
    else if (update.msg_type == 'MapCreateMessage'){
        create_map(update)
        console.log(map_list)
    }
};


function animate() {
    requestAnimationFrame( animate );
    renderer.render( scene, camera );
};

//animate();

let b = new bot({id:0,x:0,z:0,ry:0});
b.action('move', {x:0, z:0});
let v = new View3DController();
v.createCamera({left: width / - 50, right: width / 50, top: height / 50, bottom: height / - 50, near: -10000, far: 100000 })
v.attach()
v.createObject(0, 0, 0, 'avatar', 0)
