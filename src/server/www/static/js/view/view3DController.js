import * as THREE from 'three';
import {OrbitControls} from 'controls/OrbitControls';
import {GLTFLoader} from 'loaders/GLTFLoader';
import graphicObjects from "./graphicObjects.js";

export default class View3DController{
    constructor(width = window.innerWidth, height = window.innerHeight){
        this.tmp;
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
        this.createDebugGrid();
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

    createDebugGrid() {
        console.log("ici");
        const grid = new THREE.GridHelper(32, 32);
        // grid.rotateX(-Math.PI / 2);
        grid.position.set(15.5, 0.6, 15.5);
        this.scene.add(grid);
    }

    // this utility function allows you to use any three.js
    // loader with promises and async/await
    modelLoader(url) {
        return new Promise((resolve, reject) => {
            this.loader.load(url, data=> resolve(data), null, reject);
        });
    }

    createObject(x, y, z, objectName){
        var model_path = graphicObjects[objectName];

        return this.modelLoader(model_path).then(
            (gltfData) => {
                gltfData.scene.position.x = x;
                gltfData.scene.position.y = y;
                gltfData.scene.position.z = z;
                gltfData.scene.receiveShadow = true;
                gltfData.scene.castShadow = true;
                this.scene.add(gltfData.scene);
                return(gltfData.scene);
            }
        );
    }

    createBot(x, ry, z, objectName, objectIndex){
        var model_path = objectIndex === undefined? graphicObjects[objectName] : graphicObjects[objectName][objectIndex];

        return this.modelLoader(model_path).then(
            gltfData => {
                gltfData.scene.position.x = x;
                gltfData.scene.position.y = 0.5;
                gltfData.scene.position.z = z;
                gltfData.scene.rotation.y = ry;
                this.scene.add(gltfData.scene);
                return(gltfData.scene);
            }
        );
   }
}