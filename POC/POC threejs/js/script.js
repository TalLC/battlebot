import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import Stats from 'three/examples/jsm/libs/stats.module';

// Scene
const scene = new THREE.Scene();

// Caméra
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.z = 5;

// Render
const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

// Controls
const controls = new OrbitControls( camera, renderer.domElement );
controls.update();

// Light
const light = new THREE.AmbientLight( 0x404040 , 0.4); // soft white light
scene.add( light );

const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
directionalLight.position.x = -10
directionalLight.position.z =-10
scene.add( directionalLight );

// instantiate a loader
const loader = new OBJLoader();

// load a resource
loader.load(
	// resource URL
	'./Bobby_1.obj',
	// called when resource is loaded
	function ( object ) {

		scene.add( object );

	},
	// called when loading is in progresses
	function ( xhr ) {

		console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

	},
	// called when loading has errors
	function ( error ) {

		console.log( 'An error happened' );

	}
);


function animate() {
    requestAnimationFrame( animate );

    renderer.render( scene, camera );
};

animate();