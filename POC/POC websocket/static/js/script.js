import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'three/examples/jsm/libs/stats.module';

//Websocket

let ws = new WebSocket("ws://localhost:8000/ws");
var bot_obj = {};

// Scene
const scene = new THREE.Scene();

// Caméra
// const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 1000 );

let width = window.innerWidth
let height = window.innerHeight

const camera = new THREE.OrthographicCamera( width / - 2, width / 2, height / 2, height / - 2, -10000, 100000 );
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
const light = new THREE.AmbientLight( 0x404040 , 1.5); // soft white light
//scene.add( light );

const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
directionalLight.position.x = -10
directionalLight.position.z = -10
//scene.add( directionalLight );


function create_sol_map(x,z){
    // #### Load GLTF mesh file ####
    const map = new GLTFLoader()

    // Loads gltf file
    map.load(
        // resource URL
        './static/models/wall_plain.glb',

        // called when resource is loaded
        ( map ) => {
            map.scene.position.x = x
            mapp.scene.position.z = z
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

function create_big_tree(x, z){
    const tree = new GLTFLoader()

        // Loads gltf file
    tree.load(
	    // resource URL
	    './static/models/tree_big.glb',

        // called when resource is loaded
        ( tree ) => {
            tree.scene.position.x = x;
            tree.scene.position.z = z;
            scene.add(tree.scene);
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

function create_small_tree(x, z){
    const tree = new GLTFLoader()

        // Loads gltf file
    tree.load(
	    // resource URL
	    './static/models/tree_small.glb',

        // called when resource is loaded
        ( tree ) => {
            tree.scene.position.x = x;
            tree.scene.position.z = z;
            scene.add(tree.scene);
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
create_sol_map(6, -6)

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