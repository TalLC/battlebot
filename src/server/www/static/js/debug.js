import * as THREE from 'three';
import GameManager from './gameManager.js';
import DebugUi from "./debugUi.js";


export default class Debug{

    constructor(view3DController, debugContainerId) {
        this.container = document.getElementById(debugContainerId);
        this.infoContainer = this.container.querySelector("#info-container");
        this.view = view3DController;
        this.debugUi = new DebugUi(this);

        // Helpers
        // this.createCameraHelper();
        this.createDebugGrid();

        // Raycasting pour sélectionner un objet
        this.raycastedObjects = [];
        this.selectedObjectId;
        this.selectedObjectBoxHelper;
    }

    createCameraHelper() {
        this.view.scene.add( new THREE.CameraHelper( this.view.camera ) );
    }

    createDebugGrid() {
        const grid = new THREE.GridHelper(32, 32);
        grid.position.set(15.5, 0.55, 15.5);
        this.view.scene.add(grid);
    }

    updateRaycastedObjects(event) {
        const pointer = new THREE.Vector2();
        pointer.x = ( event.clientX / window.innerWidth ) * 2 - 1;
        pointer.y = - ( event.clientY / window.innerHeight ) * 2 + 1;

        // update the picking ray with the camera and pointer position
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera( pointer, this.view.camera );
        
        // calculate objects intersecting the picking ray
        this.raycastedObjects = raycaster.intersectObjects( this.view.scene.children );
    }

    clickObject(event) {
        this.deselectObject();
        
        for (const hit of this.raycastedObjects) {
            if (hit.object.type === "BoxHelper" || hit.object.type === "GridHelper") continue;
            let clickedObject;

            // On cherche si c'est un bot qui est sélectionné
            clickedObject = GameManager.getObjectFromSceneObject(hit.object.parent, "bot");
            if (clickedObject) {
                const bot = clickedObject;
                this.setSelectedObject(hit.object, bot.id);
                this.writeBotInformations(bot);
                break;
            }

            // On cherche si c'est une tile qui est sélectionné
            clickedObject = GameManager.getObjectFromSceneObject(hit.object.parent, "tile");
            if (clickedObject) {
                const obj = clickedObject;
                this.setSelectedObject(hit.object, obj.id);
                this.writeObjectInformations(obj);
                break;
            }
        }
    }

    setSelectedObject(object, id) {
        this.deselectObject();
        this.selectedObjectId = id;
        this.selectedObjectBoxHelper = new THREE.BoxHelper(object, 0xff00ff);
        this.view.scene.add(this.selectedObjectBoxHelper);
    }

    deselectObject() {
        this.selectedObjectId = undefined;
        this.resetInformationsContainer();
        if (this.selectedObjectBoxHelper) {
            this.view.disposeObject3D(this.selectedObjectBoxHelper);
        }
    }

    writeBotInformations(bot) {

        // Récupération des données
        let header = document.createElement('h1');
        header.innerHTML = `BOT`;
        
        let botId = document.createElement('h3');
        botId.innerHTML = `${bot.id}`;
        botId.style.color = `#${bot.teamColor.getHexString()}`;

        let botX = document.createElement('p');
        botX.innerHTML = `X (Bot) = ${bot.x}`;

        let botZ = document.createElement('p');
        botZ.innerHTML = `Z (Bot) = ${bot.z}`;

        let botRy = document.createElement('p');
        botRy.innerHTML = `Ry (Bot) = ${bot.ry}`;

        let botObjX = document.createElement('p');
        botObjX.innerHTML = `X (obj) = ${bot.objBot.position.x}`;

        let botObjZ = document.createElement('p');
        botObjZ.innerHTML = `Z (obj) = ${bot.objBot.position.z}`;

        let botObjRy = document.createElement('p');
        botObjRy.innerHTML = `Ry (obj) = ${bot.objBot.rotation.y}`;

        // Ajout des données au conteneur
        this.infoContainer.appendChild(header);
        this.infoContainer.appendChild(document.createElement('hr'));
        this.infoContainer.appendChild(botId);
        this.infoContainer.appendChild(botX);
        this.infoContainer.appendChild(botZ);
        this.infoContainer.appendChild(botRy);
        this.infoContainer.appendChild(botObjX);
        this.infoContainer.appendChild(botObjZ);
        this.infoContainer.appendChild(botObjRy);
    }

    writeObjectInformations(object) {
        // Récupération des données
        let header = document.createElement('h1');
        header.innerHTML = `Tile`;
        
        let objectX = document.createElement('p');
        objectX.innerHTML = `X = ${object.x}`;

        let objectZ = document.createElement('p');
        objectZ.innerHTML = `Z = ${object.z}`;

        let objectRy = document.createElement('p');
        objectRy.innerHTML = `Ry = ${object.ry}`;


        // Ajout des données au conteneur
        this.infoContainer.appendChild(header);
        this.infoContainer.appendChild(document.createElement('hr'));
        this.infoContainer.appendChild(objectX);
        this.infoContainer.appendChild(objectZ);
        this.infoContainer.appendChild(objectRy);
    }

    resetInformationsContainer() {
        // Clear du conteneur
        this.infoContainer.innerHTML = "";
    }

}