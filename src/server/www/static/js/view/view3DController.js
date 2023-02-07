import * as THREE from 'three';
import {OrbitControls} from 'controls/OrbitControls';
import {FontLoader} from 'loaders/FontLoader';
import {TextGeometry} from 'geometries/TextGeometry';


import Config from "../config.js";
import Debug from "../debug/debug.js";


export default class View3DController {
    constructor(viewContainerId, width = window.innerWidth, height = window.innerHeight){
        this.container = document.getElementById(viewContainerId);
        this.threejsCanvas = this.container.querySelector("#threejs-canvas");
        this.renderer = new THREE.WebGLRenderer( { canvas: this.threejsCanvas } );

        this.size = {width:width, height:height};
        this.renderer.setSize(this.size.width, this.size.height);
        this.scene = new THREE.Scene();
        
        let backColor = new THREE.Color(0xffffff);
        this.scene.background = backColor;

        this.initLight();
        
        this.camera = this.createCamera(
            {left: width / - 32, right: width / 32, top: height / 32, bottom: height / - 32, near: 1, far: 1000 },
            {x: 32, y: 50, z: 32},
            {x: 0, y: 0, z: 0}
        );

        if (Config.isDebug()) {
            this.debug = new Debug(this, "debug-container");
            this.container.onpointermove = this.debug.updateRaycastedObjects.bind(this.debug);
            this.container.ondblclick = this.debug.clickObject.bind(this.debug);
        }
    }

    render() {
        if (Config.isDebug()) this.debug.render();
        this.renderer.render( this.scene, this.camera );
    }

    start() {
        // Affichage du viewport Three.js
        this.container.hidden = false;

        if (Config.isDebug()) this.debug.start();
    }

    showHurtMessageForObject(obj) {
        console.log("cible", obj);

        // Affichage temporaire d'un message de Hit

        let font;

        new Promise((resolve, reject) => {
            // Load the font
            let loader = new FontLoader();
            loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/fonts/helvetiker_bold.typeface.json', function (loadedFont) {
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
            const textMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
            const textMesh = new THREE.Mesh(textGeometry, textMaterial);
            
            // Position the text in the scene
            textMesh.position.set(
                obj.x,
                obj.y + 5.0,
                obj.z
            );

            // Add the text to the scene
            this.scene.add(textMesh);
            return textMesh;
        })
        .then((textMesh) => {
            let position = textMesh.position;
            let targetY = 8.0;
            let duration = 1000;
            let startTime = performance.now();
            let moveText = function () {
                let elapsed = performance.now() - startTime;
                textMesh.position.y = position.y + (targetY - position.y) * (elapsed / duration);
                if (elapsed < duration) {
                    requestAnimationFrame(moveText);
                }
            };
            requestAnimationFrame(moveText);
          })
        .then(() => {
            // Remove the text from the scene
            this.scene.remove(textMesh);
        });
        
        // let font;

        // new Promise((resolve, reject) => {
        //     // Load the font
        //     let loader = new FontLoader();
        //     loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/fonts/helvetiker_bold.typeface.json', function (loadedFont) {
        //         font = loadedFont;
        //         resolve();
        //     });
        // })
        // .then(() => {
        //     // Create the text using TextGeometry
        //     const textGeometry = new TextGeometry("<hit>>", {
        //         font: font,
        //         size: 0.5,
        //         height: 0.001
        //     });
        //     const textMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        //     const textMesh = new THREE.Mesh(textGeometry, textMaterial);
            
        //     // Position the text in the scene
        //     textMesh.position.set(
        //         obj.x,
        //         obj.y + 5.0,
        //         obj.z
        //     );

        //     // Add the text to the scene
        //     this.scene.add(textMesh);
        
        //     return new Promise((resolve) => {
        //         setTimeout(() => {
        //             resolve(textMesh);
        //         }, 2000);
        //     });
        // })
        // .then((textMesh) => {
        //     // Remove the text from the scene
        //     this.scene.remove(textMesh);
        // });
        

        /////////////////////////////////////////////////////////////////////////////////////////////////////


        // (new FontLoader()).load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/fonts/helvetiker_bold.typeface.json', font => {
        //     const textGeometry = new TextGeometry("<hit>", {
        //         font,
        //         size: 0.5,
        //         height: 0.001
        //     });
            
        //     const textMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        //     const textMesh = new THREE.Mesh(textGeometry, textMaterial);
              
        //     // Position the text in the scene
        //     textMesh.position.set(
        //         obj.x,
        //         obj.y + 5.0,
        //         obj.z
        //     );

        //     // Add the text to the existing scene
        //     this.scene.add(textMesh);
        // }).then((resolve) => setTimeout(() => resolve(), 1000)).then(this.disposeSceneObject(textMesh))
    }

    /*
        Fonction : Permet la création/ajout à la scène de la Lumière d'ambiance, ainsi que la lumière orientée, afin de visualiser la scène
        Param : N/A
        Return : N/A
    */
    initLight(){
        console.log('initialisation light');
        //Création de la lumière ambiante
        const light = new THREE.AmbientLight( 0xffffff , 1.5);
        this.scene.add( light );

        //Création de la lumière orientée
        const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.8 );
        directionalLight.position.x = -10;
        directionalLight.position.z = -10;
        this.scene.add( directionalLight );
    }

    /*
        Fonction : Permet la création d'une camera afin de visualiser la scène
        Param : frustrum -> dictionaire definissant zone de la vision de la caméra
                position -> dictionnaire contenant la position de la caméra en x, y et z.
                lookAt -> dicitonnaire contenant le position de la ou regarde la camera en x, y et z
        Return : La caméra créé, afin de pouvoir à terme gérer plusieurs caméras.
    */
    createCamera(frustum, position, lookAt){
        console.log('initialisation cam')
        const camera = new THREE.OrthographicCamera(frustum.left, frustum.right, frustum.top, frustum.bottom, frustum.near, frustum.far );
        camera.position.set(position.x, position.y, position.z);
        camera.lookAt(lookAt.x, lookAt.y, lookAt.z);
        this.controls = new OrbitControls(camera, this.renderer.domElement);
        
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
