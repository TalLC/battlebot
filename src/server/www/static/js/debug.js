import * as THREE from 'three';
import gameManager from './gameManager.js';


export default class Debug{

    constructor(view3DController, debugContainerId) {
        this.container = document.getElementById(debugContainerId);
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
        this.resetInformationsPanel();
        
        if (this.selectedObjectBoxHelper) {
            this.view.disposeObject3D(this.selectedObjectBoxHelper);
        }

        for (const hit of this.raycastedObjects) {
            if (hit.object.type === "BoxHelper" || hit.object.type === "GridHelper") continue;
            let clickedObject;

            // On cherche si c'est un bot qui est sélectionné
            clickedObject = gameManager.getBotFromSceneObject(hit.object.parent);
            if (clickedObject) {
                this.selectedObjectBoxHelper = new THREE.BoxHelper(hit.object, 0xffff00);
                this.view.scene.add(this.selectedObjectBoxHelper);    
                this.writeBotInformations(gameManager.getBotFromSceneObject(hit.object.parent));
                break;
            }

            // // On cherche si c'est un objet de la map qui est sélectionné
            // clickedObject = gameManager.getObjectFromSceneObject(hit.object.parent);
            // if (clickedObject) {
            //     this.writeBotInformations(gameManager.getObjectFromSceneObject(hit.object.parent));
            //     break;
            // }
        }
    }

    writeBotInformations(bot) {

        // Récupération des données
        let header = document.createElement('h1');
        header.innerHTML = `BOT`;
        
        let botId = document.createElement('h2');
        botId.innerHTML = `${bot.id}`;
        botId.style.color = `#${bot.teamColor.toString(16).padStart(6, '0')}`;

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
        this.container.appendChild(header);
        this.container.appendChild(botId);
        this.container.appendChild(botX);
        this.container.appendChild(botObjX);
        this.container.appendChild(botZ);
        this.container.appendChild(botObjZ);
        this.container.appendChild(botRy);
        this.container.appendChild(botObjRy);
    }

    writeObjectInformations(object) {

    }

    resetInformationsPanel() {
        // Clear du conteneur
        this.container.innerHTML = "";
    }

}