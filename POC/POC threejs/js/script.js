import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'three/examples/jsm/libs/stats.module';

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
// renderer.setSize( 640, 480 );
document.body.appendChild( renderer.domElement );

// Controls
const controls = new OrbitControls( camera, renderer.domElement );
controls.update();

// Light
const light = new THREE.AmbientLight( 0x404040 , 1.5); // soft white light
// scene.add( light );

const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
directionalLight.position.x = -10
directionalLight.position.z =-10
// scene.add( directionalLight );

// #### Load OBJ mesh file ####
// Instantiates an obj loader
// const objloader = new OBJLoader();

// // Loads obj file
// objloader.load(
// 	// resource URL
// 	'models/Bobby_1.obj',
	
// 	// called when resource is loaded
// 	( obj ) => {
// 		scene.add( obj );
// 	},
	
// 	// called when loading is in progresses
// 	( xhr ) => {
// 		console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
// 	},
	
// 	// called when loading has errors
// 	( error ) => {
// 		console.log( 'An error happened' );
// 	}
// );

// #### Load GLTF mesh file ####
const gltfLoader = new GLTFLoader()

// Loads gltf file
gltfLoader.load(
	// resource URL
	'models/Arena_2.glb',
	
	// called when resource is loaded
	( gltf ) => {
		scene.add( gltf.scene );
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



function animate() {
    requestAnimationFrame( animate );
    renderer.render( scene, camera );
};

animate();