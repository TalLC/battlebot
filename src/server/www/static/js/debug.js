import * as THREE from 'three';
import GameManager from './gameManager.js';


export default class Debug{

    constructor(view3DController, debugContainerId) {
        this.container = document.getElementById(debugContainerId);
        this.infoContainer = this.container.querySelector("#info-container");
        this.view = view3DController;

        // Helpers
        // this.createCameraHelper();
        this.createDebugGrid();

        // Raycasting pour sélectionner un objet
        this.raycastedObjects = [];
        this.selectedObject;
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

        for (const hit of this.raycastedObjects) {
            if (hit.object.type === "BoxHelper" || hit.object.type === "GridHelper") continue;
            let clickedObject;

            // On cherche si c'est un bot qui est sélectionné
            clickedObject = GameManager.getBotFromSceneObject(hit.object.parent);
            if (clickedObject) {
                this.setSelectedObject(hit.object);
                this.writeBotInformations(GameManager.getBotFromSceneObject(hit.object.parent));
                break;
            }

            // // On cherche si c'est un objet de la map qui est sélectionné
            // clickedObject = gameManager.getObjectFromSceneObject(hit.object.parent);
            // if (clickedObject) {
            //     this.setSelectedObject(hit.object);
            //     this.writeBotInformations(gameManager.getObjectFromSceneObject(hit.object.parent));
            //     break;
            // }
        }
    }

    setSelectedObject(object) {
        this.deselectObject();
        this.selectedObjectBoxHelper = new THREE.BoxHelper(object, 0xff00ff);
        this.view.scene.add(this.selectedObjectBoxHelper);
    }

    deselectObject() {
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

        let botObjX = document.createElement('p');
        botObjX.innerHTML = `X (obj) = ${bot.objBot.position.x}`;

        let botZ = document.createElement('p');
        botZ.innerHTML = `Z (Bot) = ${bot.z}`;

        let botObjZ = document.createElement('p');
        botObjZ.innerHTML = `Z (obj) = ${bot.objBot.position.z}`;

        let botRy = document.createElement('p');
        botRy.innerHTML = `Ry (Bot) = ${bot.ry}`;

        let botObjRy = document.createElement('p');
        botObjRy.innerHTML = `Ry (obj) = ${bot.objBot.rotation.y}`;

        // Ajout des données au conteneur
        this.infoContainer.appendChild(header);
        this.infoContainer.appendChild(document.createElement('hr'));
        this.infoContainer.appendChild(botId);
        this.infoContainer.appendChild(botX);
        this.infoContainer.appendChild(botObjX);
        this.infoContainer.appendChild(botZ);
        this.infoContainer.appendChild(botObjZ);
        this.infoContainer.appendChild(botRy);
        this.infoContainer.appendChild(botObjRy);
    }

    writeObjectInformations(object) {

    }

    resetInformationsContainer() {
        // Clear du conteneur
        this.infoContainer.innerHTML = "";
    }

}