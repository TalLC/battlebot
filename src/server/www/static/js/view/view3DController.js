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
        this.renderer = new THREE.WebGLRenderer();
        this.size = {width:width, height:height};
        this.renderer.setSize(this.size.width, this.size.height);
        this.scene = new THREE.Scene();
        let backColor = new THREE.Color(0xffffff);
        this.scene.background = backColor;
        this.initLight();
        this.loader = new GLTFLoader();
        this.attach(document.body);
        this.createCamera({left: width / - 50, right: width / 50, top: height / 50, bottom: height / - 50, near: -10000, far: 100000 }, {x: 2, y: 2, z: 2}, {x: 0, y: 0, z: 0});
    }

    attach(parentElement){
        parentElement.appendChild(this.renderer.domElement);
    }

    initLight(){
        console.log('initialisation light')
        const light = new THREE.AmbientLight( 0xffffff , 1.5); // soft white light
        this.scene.add( light );

        const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
        directionalLight.position.x = -10;
        directionalLight.position.z = -10;
        this.scene.add( directionalLight );
    }

    createCamera(frustum, position, lookAt){
        console.log('initialisation cam')
        this.camera = new THREE.OrthographicCamera(frustum.left, frustum.right, frustum.top, frustum.bottom, frustum.near, frustum.far );
        this.camera.position.set(position.x, position.y, position.z);
        this.camera.lookAt(lookAt.x, lookAt.y, lookAt.z);
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.update();
        return this.camera;
    }

    createObject(x, y, z, objectName, objectIndex){
        console.log(objectName);
        if (objectName === 'air')
            return(null);
    
        // Loads gltf file
        var model_path = objectIndex === undefined? graphicObjects[objectName] : graphicObjects[objectName][objectIndex];
    
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

    // this utility function allows you to use any three.js
    // loader with promises and async/await
    modelLoader(url) {
        return new Promise((resolve, reject) => {
            this.loader.load(url, data=> resolve(data), null, reject);
        });
    }
  
    async createBot(x, y, z, objectName, objectIndex){
        var model_path = objectIndex === undefined? graphicObjects[objectName] : graphicObjects[objectName][objectIndex];

        const gltfData = await this.modelLoader(model_path);
        
        gltfData.scene.position.x = x;
        gltfData.scene.position.y = y;
        gltfData.scene.position.z = z;
        console.log("log view" + gltfData.scene);
        this.scene.add(gltfData.scene);

        return gltfData.scene;
   }
}