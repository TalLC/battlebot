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
        this.selectedObject;
    }

    render() {
        if (this.selectedObject && this.selectedObject.type === "bot") {
            this.resetInformationsContainer();
            this.writeBotInformations(this.selectedObject);
        }
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
            clickedObject = GameManager.getGameObjectFromSceneObject(hit.object.parent.parent, "bot");
            if (clickedObject) {
                const bot = clickedObject;
                this.setSelectedObject(hit.object, bot);
                this.writeBotInformations(bot);
                this.debugUi.setRemoteHidden(false);
                break;
            }

            // On cherche si c'est un objet de tuile qui est sélectionné
            clickedObject = GameManager.getGameObjectFromSceneObject(hit.object.parent, "tileObject");
            if (clickedObject) {
                const obj = clickedObject;
                this.setSelectedObject(hit.object.parent, obj);
                this.writeObjectInformations(obj);
                break;
            }

            // On cherche si c'est une tuile qui est sélectionnée
            clickedObject = GameManager.getGameObjectFromSceneObject(hit.object.parent, "tile");
            if (clickedObject) {
                const obj = clickedObject;
                this.setSelectedObject(hit.object, obj);
                this.writeObjectInformations(obj);
                break;
            }
        }
    }

    setSelectedObject(object, gameObject) {
        this.deselectObject();
        this.selectedObject = gameObject;
        this.selectedObject.debugBoxHelper = new THREE.BoxHelper(object, 0xff00ff);
        this.view.scene.add(this.selectedObject.debugBoxHelper);
    }

    deselectObject() {
        this.debugUi.setRemoteHidden(true);
        if (this.selectedObject && this.selectedObject.debugBoxHelper) {
            this.view.disposeObject3D(this.selectedObject.debugBoxHelper);
            this.selectedObject.debugBoxHelper = undefined;
        }
        this.selectedObject = undefined;
        this.resetInformationsContainer();
    }

    writeBotInformations(bot) {

        // Récupération des données
        let header = document.createElement('h1');
        header.innerHTML = `${bot.type} (${bot.modelName})`;
        
        let botId = document.createElement('h3');
        botId.innerHTML = `${bot.id}`;
        botId.style.color = `#${bot.teamColor?.getHexString()}`;

        let botX = document.createElement('p');
        botX.innerHTML = `X (Bot) = ${bot.x?.toFixed(3)}`;

        let botZ = document.createElement('p');
        botZ.innerHTML = `Z (Bot) = ${bot.z?.toFixed(3)}`;

        let botRy = document.createElement('p');
        botRy.innerHTML = `Ry (Bot) = ${bot.ry?.toFixed(3)}`;

        let botObjX = document.createElement('p');
        botObjX.innerHTML = `X (obj) = ${bot.sceneObject?.position.x.toFixed(3)}`;

        let botObjZ = document.createElement('p');
        botObjZ.innerHTML = `Z (obj) = ${bot.sceneObject?.position.z.toFixed(3)}`;

        let botObjRy = document.createElement('p');
        botObjRy.innerHTML = `Ry (obj) = ${bot.sceneObject?.rotation.y.toFixed(3)}`;

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
        header.innerHTML = `${object.type} (${object.modelName})`;
        
        let objectX = document.createElement('p');
        objectX.innerHTML = `X = ${object.x?.toFixed(3)}`;

        let objectZ = document.createElement('p');
        objectZ.innerHTML = `Z = ${object.z?.toFixed(3)}`;

        let objectRy = document.createElement('p');
        objectRy.innerHTML = `Ry = ${object.ry?.toFixed(3)}`;

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