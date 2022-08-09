import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'three/examples/jsm/libs/stats.module';

//Websocket

let ws = new WebSocket("ws://localhost:8000/ws");
var bot_obj = {};
var obj_list = {
    'small_tree':'tree_small.glb',
    'big_tree':'tree_big.glb',
    'sol':'sol.glb',
    'eau':'eau.glb'
};

// Scene
const scene = new THREE.Scene();

// Caméra
// const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 1000 );

let width = window.innerWidth
let height = window.innerHeight

const camera = new THREE.OrthographicCamera( width / - 50, width / 50, height / 50, height / - 50, -10000, 100000 );
camera.position.set(2, 2, 2);
camera.lookAt(0, 0, 0)


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
directionalLight.position.x = -10
directionalLight.position.z = -10
scene.add( directionalLight );

function create_object(name, x, z){
    // #### Load GLTF mesh file ####
    const map = new GLTFLoader()

    // Loads gltf file
    var object = './static/models/' + obj_list[name]
    map.load(
        // resource URL
        object,

        // called when resource is loaded
        ( map ) => {
            map.scene.position.x = x
            map.scene.position.z = z
            scene.add( map.scene );
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


function create_bot(name, x, z){
    const bot = new GLTFLoader()

        // Loads gltf file
    bot.load(
	    // resource URL
	    './static/models/robot_1.glb',

        // called when resource is loaded
        ( bot ) => {
            bot.scene.position.x = x;
            bot.scene.position.z = z;
            bot_obj[name] = bot.scene;
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
create_object('sol' , 0, 0)
create_object('sol' , 0, 2)
create_object('sol' , 0, 4)
create_object('sol' , 0, 6)
create_object('sol' , 0, 8)
create_object('sol' , 0, 10)
create_object('sol' , 0, -2)
create_object('sol' , 0, -4)
create_object('sol' , 0, -6)
create_object('sol' , 0, -8)
create_object('sol' , 0, -10)
create_object('sol' , 2, 0)
create_object('sol' , 2, 2)
create_object('sol' , 2, 4)
create_object('sol' , 2, 6)
create_object('sol' , 2, 8)
create_object('sol' , 2, 10)
create_object('sol' , 2, -2)
create_object('sol' , 2, -4)
create_object('sol' , 2, -6)
create_object('sol' , 2, -8)
create_object('sol' , 2, -10)
create_object('sol' , 4, 0)
create_object('sol' , 4, 2)
create_object('sol' , 4, 4)
create_object('sol' , 4, 6)
create_object('sol' , 4, 8)
create_object('sol' , 4, 10)
create_object('sol' , 4, -2)
create_object('sol' , 4, -4)
create_object('sol' , 4, -6)
create_object('sol' , 4, -8)
create_object('sol' , 4, -10)
create_object('sol' , 6, 0)
create_object('sol' , 6, 2)
create_object('sol' , 6, 4)
create_object('sol' , 6, 6)
create_object('sol' , 6, 8)
create_object('sol' , 6, 10)
create_object('sol' , 6, -2)
create_object('sol' , 6, -4)
create_object('sol' , 6, -6)
create_object('sol' , 6, -8)
create_object('sol' , 6, -10)
create_object('sol' , 8, 0)
create_object('sol' , 8, 2)
create_object('sol' , 8, 4)
create_object('sol' , 8, 6)
create_object('sol' , 8, 8)
create_object('sol' , 8, 10)
create_object('sol' , 8, -2)
create_object('sol' , 8, -4)
create_object('sol' , 8, -6)
create_object('sol' , 8, -8)
create_object('sol' , 8, -10)
create_object('sol' , 10, 0)
create_object('sol' , 10, 2)
create_object('sol' , 10, 4)
create_object('sol' , 10, 6)
create_object('sol' , 10, 8)
create_object('sol' , 10, 10)
create_object('sol' , 10, -2)
create_object('sol' , 10, -4)
create_object('sol' , 10, -6)
create_object('sol' , 10, -8)
create_object('sol' , 10, -10)
create_object('sol' , -2, 0)
create_object('sol' , -2, 2)
create_object('sol' , -2, 4)
create_object('sol' , -2, 6)
create_object('sol' , -2, 8)
create_object('sol' , -2, 10)
create_object('sol' , -2, -2)
create_object('sol' , -2, -4)
create_object('sol' , -2, -6)
create_object('sol' , -2, -8)
create_object('sol' , -2, -10)
create_object('sol' , -4, 0)
create_object('sol' , -4, 2)
create_object('sol' , -4, 4)
create_object('sol' , -4, 6)
create_object('sol' , -4, 8)
create_object('sol' , -4, 10)
create_object('sol' , -4, -2)
create_object('sol' , -4, -4)
create_object('sol' , -4, -6)
create_object('sol' , -4, -8)
create_object('sol' , -4, -10)
create_object('sol' , -6, 0)
create_object('sol' , -6, 2)
create_object('sol' , -6, 4)
create_object('sol' , -6, 6)
create_object('sol' , -6, 8)
create_object('sol' , -6, 10)
create_object('sol' , -6, -2)
create_object('sol' , -6, -4)
create_object('sol' , -6, -6)
create_object('sol' , -6, -8)
create_object('sol' , -6, -10)
create_object('sol' , -8, 0)
create_object('sol' , -8, 2)
create_object('sol' , -8, 4)
create_object('sol' , -8, 6)
create_object('sol' , -8, 8)
create_object('sol' , -8, 10)
create_object('sol' , -8, -2)
create_object('sol' , -8, -4)
create_object('sol' , -8, -6)
create_object('sol' , -8, -8)
create_object('sol' , -8, -10)
create_object('sol' , -10, 0)
create_object('sol' , -10, 2)
create_object('sol' , -10, 4)
create_object('sol' , -10, 6)
create_object('sol' , -10, 8)
create_object('sol' , -10, 10)
create_object('sol' , -10, -2)
create_object('sol' , -10, -4)
create_object('sol' , -10, -6)
create_object('sol' , -10, -8)
create_object('sol' , -10, -10)
create_object('big_tree' , -6, 2)


create_bot('bot1', 6, -6)

function update_bot(bot, move)
{
    if (bot)
    {
        bot.rotateY(parseFloat(move.rotateY));
        bot.position.x = move.x;
        bot.position.z = move.z;
    }
};

ws.onmessage = function(event)
{
    var move = JSON.parse(event.data)
    console.log(move)
    update_bot(bot_obj['bot1'], move)
};

function animate() {
    requestAnimationFrame( animate );
    renderer.render( scene, camera );
};

animate();