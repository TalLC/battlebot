import * as THREE from './three.module.js';
import {OrbitControls} from './OrbitControls.js';
import {OBJLoader} from './OBJLoader.js';
import {GLTFLoader} from './GLTFLoader.js';
import Stats from './stats.module.js';
import graphicObjects from "./graphicObjects.js";

export default class View3DController{
    scene;
    size;
    camera;
    renderer;
    controls;
    light;
    loader;
    constructor(width = window.innerWidth, height = window.innerHeight){
        this.scene = new THREE.Scene();
        this.size = {width:width, height:height};
        this.renderer = new THREE.WebGLRenderer();
        this.renderer.setSize(this.size.width, this.size.height);
        this.initLight();
        this.loader = new GLTFLoader();
    }

    attach(parentElement){
        parentElement.appendChild(this.renderer.domElement);
    }

    initLight(){
        const light = new THREE.AmbientLight( 0xffffff , 1.5); // soft white light
        this.scene.add( light );

        const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
        directionalLight.position.x = -10;
        directionalLight.position.z = -10;
        this.scene.add( directionalLight );
    }

    createCamera(frustum, position, lookAt){
        this.camera = new THREE.OrthographicCamera(frustum.left, frustum.right, frustum.top, frustum.bottom, frustum.near, frustum.far );
        this.camera.position.set(position.x, position.y, position.z);
        this.camera.lookAt(lookAt.x, lookAt.y, lookAt.z);
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.update();
        return this.camera;
    }

    createObject(x, y, z, objectName, objectIndex){
        console.log(objectName)
        if (objectName === 'air')
            return(null)
    
        // Loads gltf file
        var model_path = objectIndex === undefined? graphicObjects[objectName] : graphicObjects[objectName][objectIndex]
    
        this.loader.load(
            // resource URL
            model_path,
    
            // called when resource is loaded
            (map_object) => {
                map_object.scene.position.x = x;
                map_object.scene.position.y = y;
                map_object.scene.position.z = z;
                this.scene.add( map_object.scene );
            },
    
            // called when loading is in progresses
            ( xhr ) => {
                console.debug( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
            },
    
            // called when loading has errors
            ( error ) => {
                console.error( 'unable to create objects ' + objectName + " : " + error.name + ", " + error.message);
            }
        );
    }
}