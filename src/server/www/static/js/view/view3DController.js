import * as THREE from 'three';
import {OrbitControls} from 'controls/OrbitControls';
import {GLTFLoader} from 'loaders/GLTFLoader';
import graphicObjects from "./graphicObjects.js";
import Debug from "../debug.js";

export default class View3DController{
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
        // this.attach(this.container);
        this.camera = this.createCamera(
            {left: width / - 50, right: width / 50, top: height / 50, bottom: height / - 50, near: -10000, far: 100000 },
            {x: 32, y: 50, z: 32},
            {x: 0, y: 0, z: 0}
        );

        this.debug = new Debug(this, "debug-container");
        this.container.onpointermove = this.debug.updateRaycastedObjects.bind(this.debug);
        this.container.onclick = this.debug.clickObject.bind(this.debug);
        this.container.ondblclick = this.debug.deselectObject.bind(this.debug);
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
        Fonction : Permet la création/ajout à la scène d'un objet est appelé à chaque nouvelle objet (Arbre, Mur, Rocher, Sol, Eau...).
        Param : x -> Position en x de l'objet
                y -> Position en y de l'objet
                z -> Position en z de l'objet
                objectName -> Nom de l'objet à créer
        Return :  Une Promise qui retournera à terme l'objet de la scene afin de pouvoir intéragir avec en cas de destruction par exemple.
    */
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

    /*
        Fonction : Permet la création/ajout à la scène d'un objet Bot est appelé à chaque nouveau Bot.
        Param : x -> Position en x du Bot
                z -> Position en z du Bot
                ry -> Rotation autour de l'Axe y du Bot
                objectName -> Nom de la liste contenant les différents avatars, on pourra imaginer plusieurs listes différentes pour différentes MAP ou équipes.
                objectIndex -> Index correspondant à l'avatar souhaité dans la liste.
        Return : Une Promise qui retournera à terme l'objet Bot de la scene afin de pouvoir intéragir avec.
    */
    createBot(x, ry, z, teamColor, objectName, objectIndex){
        var model_path = objectIndex === undefined? graphicObjects[objectName] : graphicObjects[objectName][objectIndex];

        return this.modelLoader(model_path).then(
            gltfData => {
                gltfData.scene.position.x = x;
                gltfData.scene.position.y = 0.5;
                gltfData.scene.position.z = z;
                gltfData.scene.rotation.y = ry;
                
                const material = new THREE.MeshBasicMaterial(
                    {
                        "color": teamColor,
                        "transparent": true,
                        "opacity": 0.7
                    }
                );

                gltfData.scene.traverse((o) => {
                    if (o.isMesh) o.material = material;
                });

                this.scene.add(gltfData.scene);
                return(gltfData.scene);
            }
        );
   }

    disposeObject3D(object3D) {
        if (!(object3D instanceof THREE.Object3D)) return false;

        // for better memory management and performance
        if (object3D.geometry) object3D.geometry.dispose();

        if (object3D.material) {
            if (object3D.material instanceof Array) {
                // for better memory management and performance
                object3D.material.forEach(material => material.dispose());
            } else {
                // for better memory management and performance
                object3D.material.dispose();
            }
        }
        object3D.removeFromParent(); // the parent might be the scene or another Object3D, but it is sure to be removed this way
    }

}