import * as THREE from 'three';
import { OrbitControls } from 'controls/OrbitControls';
import { FontLoader } from 'loaders/FontLoader';
import { TextGeometry } from 'geometries/TextGeometry';
import GameConfig from '../config.js';
import Debug from "../debug/debug.js";


export default class View3DController {
    constructor(viewContainerId, width = window.innerWidth, height = window.innerHeight){
        this.container = document.getElementById(viewContainerId);
        this.threejsCanvas = this.container.querySelector("#threejs-canvas");
        this.renderer = new THREE.WebGLRenderer( { canvas: this.threejsCanvas } );

        this.size = {width:width, height:height};
        this.renderer.setSize(this.size.width, this.size.height);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        this.scene = new THREE.Scene();
	    this.scene.background = new THREE.Color( 0xa0d0da );
	    this.scene.fog = new THREE.Fog( 0xa0d0da, 0.5, 500);

        this.initLight();

        // Camera OrthographicCamera
        // this.camera = this.createCamera(
        //     {left: width / - 32, right: width / 32, top: height / 32, bottom: height / - 32, near: 1, far: 1000 },
        //     {x: 32, y: 50, z: 32},
        //     {x: 0, y: 0, z: 0}
        // );

        // Création de la caméra
        this.camera = this.createCamera(
            {x: 64, y: 64, z: 64},
            {x: 16, y: 0, z: 16}
        );

        // Prise en charge du redimensionnement de fenêtre
        window.onresize = this.resize.bind(this);

        if (GameConfig().isDebug) {
            this.debug = new Debug(this, "debug-container");
            this.container.onpointermove = this.debug.updateRaycastedObjects.bind(this.debug);
            this.container.ondblclick = this.debug.clickObject.bind(this.debug);
        }

    }

    render() {
        if (GameConfig().isDebug) this.debug.render();
        this.renderer.render( this.scene, this.camera );
    }

    resize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.render();
    }

    start() {
        // Affichage du viewport Three.js
        this.container.hidden = false;

        if (GameConfig().isDebug) this.debug.start();
    }

    showHurtMessageForObject(obj) {
        let font;

        new Promise((resolve) => {
            // Load the font
            let loader = new FontLoader();
            loader.load('static/fonts/helvetiker_bold.typeface.json', function (loadedFont) {
                font = loadedFont;
                resolve();
            });
        })
        .then(() => {
            // Create the text using TextGeometry
            const textGeometry = new TextGeometry("<hit>", {
                font: font,
                size: 0.5,
                height: 0.001
            });
            const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00, transparent: true });
            const textMesh = new THREE.Mesh(textGeometry, textMaterial);

            // Position the text in the scene
            textMesh.position.set(
                obj.x,
                obj.y + 5.0,
                obj.z
            );
            textMesh.lookAt(this.camera.position);
            
            // Add the text to the scene
            this.scene.add(textMesh);
            return textMesh;
        })
        .then((textMesh) => {
            // Diminuer l'opcatier pour rendre le texte invisible
            return new Promise((resolve) => {
                let opacity = 1;
                const interval = setInterval(() => {
                    opacity -= 0.1;
                    textMesh.material.opacity = opacity;
                    textMesh.lookAt(this.camera.position);
                    if (opacity <= 0) {
                        clearInterval(interval);
                        resolve(textMesh);
                    }
                }, 100);
            });
        })
        .then((textMesh) => {
            // Supprimer l'objet de la scene
            this.disposeSceneObject(textMesh);
        });
    }

    /*
        Fonction : Permet la création/ajout à la scène de la Lumière d'ambiance, ainsi que la lumière orientée, afin de visualiser la scène
        Param : N/A
        Return : N/A
    */
    initLight(){
        console.log('initialisation light');
        //Création de la lumière ambiante
        const light = new THREE.AmbientLight(0xffffff, 0.9);
        this.scene.add( light );

        //Création de la lumière orientée
        const directionalLight = new THREE.DirectionalLight(0xe6faff, 1.0);
        directionalLight.position.x = 8.0;
        directionalLight.position.y = 16.0;
        directionalLight.position.z = 8.0;
        directionalLight.target.position.set(16, 0, 16);
        directionalLight.target.updateMatrixWorld();
        directionalLight.castShadow = true;
        directionalLight.shadow.camera.top = 32;
        directionalLight.shadow.camera.bottom = -32;
        directionalLight.shadow.camera.left = 32;
        directionalLight.shadow.camera.right = -32;
        directionalLight.shadow.bias = -0.01;

        directionalLight.shadow.mapSize.width = 1024; // default
        directionalLight.shadow.mapSize.height = 1024; // default
        directionalLight.shadow.camera.near = 0.001; // default
        directionalLight.shadow.camera.far = 55;
        directionalLight.shadow.radius = 1;
        this.scene.add(directionalLight);

        // if (GameConfig().isDebug) {
        //     const dlHelper = new THREE.DirectionalLightHelper(directionalLight, 3);
        //     this.scene.add(dlHelper);

        //     const shadowCameraHelper = new THREE.CameraHelper(directionalLight.shadow.camera);
        //     this.scene.add(shadowCameraHelper);
        // }
    }

    /*
        Fonction : Permet la création d'une camera afin de visualiser la scène
        Param : frustrum -> dictionnaire definissant zone de la vision de la caméra
                position -> dictionnaire contenant la position de la caméra en x, y et z.
                lookAt -> dicitonnaire contenant le position de la ou regarde la camera en x, y et z
        Return : La caméra créé, afin de pouvoir à terme gérer plusieurs caméras.
    */
    createCamera(position, lookAt){
        console.log('initialisation cam')
        const camera = new THREE.PerspectiveCamera(18, window.innerWidth / window.innerHeight, 1, 500);
        // const camera = new THREE.OrthographicCamera(frustum.left, frustum.right, frustum.top, frustum.bottom, frustum.near, frustum.far );
        camera.position.set(position.x, position.y, position.z);
        this.controls = new OrbitControls(camera, this.renderer.domElement);
        this.controls.target.set(lookAt.x, lookAt.y, lookAt.z);

        this.controls.update();
        return camera;
    }

    /*
        Fonction : Efface complètement un objet de la scène ThreeJs.
        Param : sceneObject -> L'objet à supprimer.
        Return : N/A
    */
    disposeSceneObject(sceneObject) {
        if (!(sceneObject instanceof THREE.Object3D)) return false;

        // for better memory management and performance
        if (sceneObject.geometry) sceneObject.geometry.dispose();

        if (sceneObject.material) {
            if (sceneObject.material instanceof Array) {
                // for better memory management and performance
                sceneObject.material.forEach(material => material.dispose());
            } else {
                // for better memory management and performance
                sceneObject.material.dispose();
            }
        }
        sceneObject.removeFromParent(); // the parent might be the scene or another Object3D, but it is sure to be removed this way
    }

}