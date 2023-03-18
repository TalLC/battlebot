import * as THREE from 'three';
import * as TWEEN from 'tween';
import logger from '../logger.js';
import { OrbitControls } from 'controls/OrbitControls';
import { FontLoader } from 'loaders/FontLoader';
import { TextGeometry } from 'geometries/TextGeometry';
import { updateMessageQueue } from '../messages/messageHandler.js'
import Object3DFactory from "./object3DFactory.js";
import GameConfig from '../config.js';
import Debug from "../debug/debug.js";


export default class View3DController {
    constructor(gameManager, viewContainerId, width = window.innerWidth, height = window.innerHeight){
        this.gameManager = gameManager;
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

        // On bind l'instance courante à cette fonction car elle fait de l'appel récursif
        this.animate = this.animate.bind(this);
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

    /*
        Fonction : Permet l'affichage de la scene.
        Param : N/A
        Return : N/A
    */
    animate() {
        if(updateMessageQueue[0] !== undefined && updateMessageQueue[0].messages !== undefined) {
            let promises = [];
            // logger.debug(updateMessageQueue[0].messages)
            for(let i = 0; i < updateMessageQueue[0].messages.length; i++){
                promises.push(
                    this.gameManager.doAction(updateMessageQueue[0].messages[i])
                );
            }
            Promise.all(promises).then(() => {
                window.requestAnimationFrame( this.animate );
                TWEEN.update();
                this.gameManager.render();
            });
            updateMessageQueue.shift();
        } else {
            window.requestAnimationFrame( this.animate );
            TWEEN.update();
            this.gameManager.render();
        }
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

    
    /**
     * Fonction qui affiche le tir du bot.
     * @param {Object} bot - Le bot qui tire.
     * @param {Object} to - Les coordonnées de la cible.
     * @returns {void} Cette fonction ne retourne rien.
     */
    shootTo(bot, to) {
        const laserMesh = Object3DFactory.createLaserMesh(
            bot.teamColor,
            [bot.x, 1.5, bot.z],
            [to.x, 1.5, to.z]
        );

        // Ajout du mesh à la scène
        this.gameManager.viewController.scene.add(laserMesh);

        // Création d'une promesse qui se résout après 1 seconde
        const laserPromise = new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, 1000);
        });

        // Attente de la résolution de la promesse, puis suppression du mesh de la scène
        laserPromise.then(() => {
            this.gameManager.viewController.disposeSceneObject(laserMesh);
        });
    }


    /*
        Fonction : Permet la création/ajout à la scène de la Lumière d'ambiance, ainsi que la lumière orientée, afin de visualiser la scène
        Param : N/A
        Return : N/A
    */
    initLight(){
        logger.debug('initialisation light');
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
        logger.debug('initialisation cam')
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
