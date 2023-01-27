import * as THREE from 'three';
import {OrbitControls} from 'controls/OrbitControls';
import {GLTFLoader} from 'loaders/GLTFLoader';
import graphicObjects from "./graphicObjects.js";
import Debug from "../debug.js";


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
        this.loader = new GLTFLoader();
        
        this.camera = this.createCamera(
            {left: width / - 32, right: width / 32, top: height / 32, bottom: height / - 32, near: 1, far: 1000 },
            {x: 32, y: 50, z: 32},
            {x: 0, y: 0, z: 0}
        );

        this.debug = new Debug(this, "debug-container");
        
        this.container.onpointermove = this.debug.updateRaycastedObjects.bind(this.debug);
        this.container.ondblclick = this.debug.clickObject.bind(this.debug);
    }

    render() {
        this.debug.render();
        this.renderer.render( this.scene, this.camera );
    }

    /*
        Fonction : Permet l'affichage sur notre page html du ThreeJS
        Param : parentElement -> correspondant au body de notre page html
        Return : N/A
    */
    attach(parentElement){
        parentElement.appendChild(this.renderer.domElement);
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
        Fonction : Permet la création d'une Promise qui sera utilisé pour la création des Objets 3D.
        Param : obj -> Nom de l'objet à ajouter à la scene.
        Return :  Une Promise qui servira à la création et ajout à la scène des Objets 3D
    */
    modelLoader(obj) {
        return new Promise((resolve, reject) => {
            this.loader.load(obj, data=> resolve(data), null, reject);
        });
    }

    /*
        Fonction : Permet la création/ajout à la scène d'un objet. Est appelé à chaque nouvel objet (Arbre, Mur, Rocher, Sol, Eau...).
        Param : x -> Position en x de l'objet
                y -> Position en y de l'objet
                z -> Position en z de l'objet
                ry -> Rotation en y de l'objet
                modelPath -> Chemin du fichier 3D à charger
        Return :  Une Promise qui retournera à terme l'objet de la scene afin de pouvoir intéragir avec en cas de destruction par exemple.
    */
    createObject(x, y, z, ry, modelPath) {
        return this.modelLoader(modelPath).then(
            (gltfData) => {
                gltfData.scene.position.x = x;
                gltfData.scene.position.y = y;
                gltfData.scene.position.z = z;
                gltfData.scene.rotation.y = ry;
                gltfData.scene.receiveShadow = true;
                gltfData.scene.castShadow = true;
                this.scene.add(gltfData.scene);
                return(gltfData.scene);
            }
        );
    }

    /*
        Fonction : Permet la création/ajout d'un objet Bot à la scène.
        Param : bot -> L'objet Bot dont on veut créer le modèle 3D
        Return : Une Promise qui retournera à terme le modèle 3D afin de pouvoir intéragir avec.
    */
    createBot3D(bot) {
        const modelPath = bot.modelName === undefined? graphicObjects['avatar']['default'] : graphicObjects['avatar'][bot.modelName];
        return this.createObject(bot.x, bot.y, bot.z, bot.ry, modelPath).then(sceneObject => {
            // Peinture du bot de la couleur de l'équipe
            const material = new THREE.MeshBasicMaterial(
                {
                    "color": bot.teamColor,
                    "transparent": true,
                    "opacity": 0.7
                }
            );

            sceneObject.traverse((o) => {
                if (o.isMesh) o.material = material;
            });

            bot.sceneObject = sceneObject;
        });
    }

    /*
        Fonction : Permet la création/ajout d'un objet 3D à la scène (tile, tile object, ...).
        Param : mapObject -> L'objet MapObject dont on veut créer le modèle 3D
        Return : Une Promise qui retournera à terme le modèle 3D afin de pouvoir intéragir avec.
    */
    createMapObject3D(mapObject) {
        const modelPath = graphicObjects[mapObject.modelName];
        if (modelPath) {
            this.createObject(mapObject.x, mapObject.y, mapObject.z, mapObject.ry, modelPath).then(sceneObject => {
                mapObject.sceneObject = sceneObject;
            });
        }
    }

    /*
        Fonction : Efface complètement un objet de la scène ThreeJs.
        Param : sceneObject -> L'objet à supprimer.
        Return : N/A
    */
    disposeObject3D(sceneObject) {
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