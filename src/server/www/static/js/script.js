import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'three/examples/jsm/libs/stats.module';

//Websocket

let ws = new WebSocket("ws://localhost:8000/ws");
var BOTS = new Object();
var obj_list = {
    'tree': 'tree.glb',
    'rock': 'rock.glb',
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
const scene = new THREE.Scene();
const color_bg = new THREE.Color( 'skyblue' );
scene.background = color_bg;

// Model loader
const model_loader = new GLTFLoader();

// Caméra
//const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 1000 );

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

    if (name == 'air')
        return(null)

    // #### Load GLTF mesh file ####
    const loader = new GLTFLoader()

    // Loads gltf file
    var model_path = './static/models/' + obj_list[name]
    var loaded_object = null

    loader.load(
        // resource URL
        model_path,

        // called when resource is loaded
        ( map_object ) => {
            map_object.scene.position.x = x;
            map_object.scene.position.y = y;
            map_object.scene.position.z = z;
            loaded_object = map_object;
            scene.add( map_object.scene );
        },

        // called when loading is in progresses
        ( xhr ) => {
            console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
        },

        // called when loading has errors
        ( error ) => {
            console.log( 'An error happened' );
        }
    );
    return(loaded_object);
}

// this utility function allows you to use any three.js
// loader with promises and async/await
function modelLoader(url) {
  return new Promise((resolve, reject) => {
    model_loader.load(url, data=> resolve(data), null, reject);
  });
}

async function create_bot(x, z) {
    const gltfData = await modelLoader('./static/models/robot_1.glb')
    
    scene.add(gltfData.scene);
 
    return gltfData.scene;
 }
 

// async function create_bot(x, z) {
//     var bot = null
//     const loader = new GLTFLoader()


//     loader.OnLoaded 

//     const result = await loader.loadAsync('./static/models/robot_1.glb');
//     console.log("result", result)

//     // Loads gltf file
//     loader.load(
// 	    // resource URL
// 	    './static/models/robot_1.glb',

//         // called when resource is loaded
//         ( bot_object ) => {
//             bot_object.scene.position.x = x;
//             bot_object.scene.position.z = z;
//             bot = bot_object.scene
//             scene.add(bot);
//         },

//         // called when loading is in progresses
//         ( xhr ) => {
//             console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
//         },

//         // called when loading has errors
//         ( error ) => {
//             console.log( 'An error happened' );
//         }
//     );

//     // while(bot == null) {
//     //     console.log("sleep")
        
//     // }

//     console.log(bot);

//     return bot;
// }

function create_bot_shield(id_bot, x, z){
    const bot_shield = new GLTFLoader()

        // Loads gltf file
    bot_shield.load(
	    // resource URL
	    './static/models/robot_shield.glb',

        // called when resource is loaded
        ( bot_shield ) => {
            bot_shield.scene.position.x = x;
            bot_shield.scene.position.z = z;
            scene.add(bot.scene);
        },

        // called when loading is in progresses
        ( xhr ) => {
            console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
        },

        // called when loading has errors
        ( error ) => {
            console.log( 'An error happened' );
        }
    );
}

function create_bot_hit(id_bot, x, z){
    const bot_shield = new GLTFLoader()

        // Loads gltf file
    bot_shield.load(
	    // resource URL
	    './static/models/robot_hit.glb',

        // called when resource is loaded
        ( bot_shield ) => {
            bot_shield.scene.position.x = x;
            bot_shield.scene.position.z = z;
            scene.add(bot.scene);
        },

        // called when loading is in progresses
        ( xhr ) => {
            console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
        },

        // called when loading has errors
        ( error ) => {
            console.log( 'An error happened' );
        }
    );
}

function create_shoot(x_origin, z_origin, x_target, z_target){
    const material = new THREE.LineBasicMaterial( { color: 0xff0000 } );

    const points = [];
    points.push( new THREE.Vector3( x_origin, 3, z_origin ) );
    points.push( new THREE.Vector3( x_target, 3, z_target ) );

    const geometry = new THREE.BufferGeometry().setFromPoints( points );
    const line = new THREE.Line( geometry, material );
    scene.add( line );
}

function delete_object(object){
    console.log("delete_object")
}

async function update_bot(update) {

    console.log(update.bot_id)
    if (!(update.bot_id in BOTS)) {
        BOTS[update.bot_id] = await create_bot(update.x, update.z)
    }

    var bot = BOTS[update.bot_id]
    console.log(bot)

    if (update.y){ bot.rotation.y = update.y };
    if (update.x){ bot.position.x = update.x };
    if (update.z){ bot.position.z = update.z };
    if (update.action & EnumStatus.SHOOTING) {
        for (var target in update.targets) {
            create_shoot(bot.position.x, bot.position.z, target.x, target.z)
        }
    };
    if (update.action & EnumStatus.SHIELD_HIDE)
    { 
        
    };
    if (update.action & EnumStatus.SHIELD_SHOW)
    {
        create_bot_shield(update.id_bot, update.x, update.z)
    };

};

function update_map(update){
    if (map_list[update.x][update.z])
    {
        delete(update.tile_object)
        create_object(update.tile_object, update.x * 2, 1, update.z * 2)
    }
    else
    {
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
    var update = JSON.parse(event.data);

    if (update.msg_type == 'BotUpdateMessage') {
        update_bot(update)
    }
    else if (update.msg_type == 'MapUpdateMessage')
        update_map(update)
    else if (update.msg_type == 'MapCreateMessage')
        // create map
        create_map(update)
        //update camera
        camera.lookAt(update.height, 0, update.width);
        controls.target.set(update.height, 0, update.width)
};

function animate() {
    requestAnimationFrame( animate );
    renderer.render( scene, camera );
};

animate();