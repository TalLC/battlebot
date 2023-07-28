import * as THREE from "three";
import GameManager from "../gameManager.js";
import MapManager from "../mapManager.js";
import DebugUi from "./debugUi.js";

export default class Debug {
    /**
     * Constructeur de la classe Debug.
     * @param {View3DController} view3DController - Contrôleur de la vue 3D.
     * @param {string} debugContainerId - Identifiant du conteneur pour l'affichage des informations de débogage.
     */
    constructor(view3DController, debugContainerId) {
        this.container = document.getElementById(debugContainerId);
        this.infoContainer = this.container.querySelector("#info-container-text");
        this.view = view3DController;
        this.debugUi = new DebugUi(this, view3DController);

        // Raycasting pour sélectionner un objet
        this.raycastedObjects = [];
        this.selectedObject;

        // A exécuter après le chargement de la map
        this.waitForMapLoaded();
    }

    /**
     * Fonction dont le contenu est exécuté lorsque la carte a été chargée par le MapManager.
     */
    waitForMapLoaded() {
        MapManager.mapLoadedPromise.then(() => {
            this.createDebugGrid();
        });
    }

    /**
     * Fonction de rendu de la classe Debug.
     * Affiche les informations du bot sélectionné s'il y en a un.
     */
    render() {
        if (this.selectedObject && this.selectedObject.type === "bot") {
            this.resetInformationsContainer();
            this.writeBotInformations(this.selectedObject);
        }
    }

    /**
     * Fonction de démarrage de la classe Debug.
     * Affiche le conteneur d'informations de débogage.
     */
    start() {
        // Affichage des informations de debug
        this.container.hidden = false;
    }

    /**
     * Fonction pour créer un helper pour la caméra.
     * Non utilisée pour l'instant.
     */
    createCameraHelper() {
        this.view.scene.add(new THREE.CameraHelper(this.view.globalCamera));
    }

    /**
     * Fonction pour créer une grille de débogage dans la scène.
     */
    createDebugGrid() {
        const grid = new THREE.GridHelper(MapManager.height, MapManager.width);
        grid.position.set((MapManager.height - 1) / 2, 0.55, (MapManager.width - 1) / 2);
        this.view.scene.add(grid);
    }

    /**
     * Fonction pour mettre à jour les objets raycastés lors d'un clic.
     * @param {Event} event - Événement de clic de souris.
     */
    updateRaycastedObjects(event) {
        const pointer = new THREE.Vector2();
        pointer.x = (event.clientX / this.view.container.offsetWidth) * 2 - 1;
        pointer.y = -(event.clientY / this.view.container.offsetHeight) * 2 + 1;

        // Tir d'un rayon de la caméra vers la position du curseur
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(pointer, this.view.getCurrentCamera());

        // Récupération des objets touchés par le rayon
        this.raycastedObjects = raycaster.intersectObjects(this.view.scene.children);
    }

    /**
     * Sélectionne un objet en effectuant un raycast sur les objets de la scène à partir de la position de la souris.
     * Si un objet est trouvé, on affiche ses informations dans le conteneur de debug.
     * Cliquer dans le vide désélectionne l'objet précédemment sélectionné.
     * @param {MouseEvent} event - L'événement de click de souris.
     */
    clickObject(event) {
        // Désélectionne l'objet précédemment sélectionné
        this.deselectObject();

        // Effectue le raycast sur les objets de la scène
        for (const hit of this.raycastedObjects) {
            if (hit.object.type === "BoxHelper" || hit.object.type === "GridHelper") continue;
            let clickedObject;
            
            // On cherche si c'est un bot qui est sélectionné
            clickedObject = GameManager().getGameObjectFromSceneObject(hit.object.parent.parent, "bot");
            if (clickedObject) {
                const bot = clickedObject;
                this.setSelectedObject(hit.object.parent, bot);
                this.writeBotInformations(bot);
                this.debugUi.setRemoteHidden(false);
                break;
            }

            // On cherche si c'est un objet de tuile qui est sélectionné
            clickedObject = GameManager().getGameObjectFromSceneObject(hit.object.parent, "tileObject");
            if (clickedObject) {
                const obj = clickedObject;
                this.setSelectedObject(hit.object.parent, obj);
                this.writeObjectInformations(obj);
                break;
            }

            // On cherche si c'est une tuile qui est sélectionnée
            clickedObject = GameManager().getGameObjectFromSceneObject(hit.object.parent, "tile");
            if (clickedObject) {
                const obj = clickedObject;
                this.setSelectedObject(hit.object, obj);
                this.writeObjectInformations(obj);
                break;
            }
        }
    }

    /**
     * Sélectionne l'objet spécifié et affiche une boîte de débogage autour de celui-ci.
     * @param {THREE.Object3D} object - L'objet à sélectionner.
     * @param {GameObject} gameObject - Le GameObject correspondant à l'objet sélectionné.
     */
    setSelectedObject(object, gameObject) {
        this.deselectObject();
        this.selectedObject = gameObject;

        // Création d'une boîte de débogage et ajout à la scène
        this.selectedObject.debugBoxHelper = new THREE.BoxHelper(object, 0xff00ff);
        this.view.scene.add(this.selectedObject.debugBoxHelper);
    }

    /**
     * Désélectionne l'objet actuellement sélectionné et cache sa boîte de débogage.
     */
    deselectObject() {
        this.debugUi.setRemoteHidden(true);

        if (this.selectedObject && this.selectedObject.debugBoxHelper) {
            // Suppression de la boîte de débogage de la scène
            this.view.disposeSceneObject(this.selectedObject.debugBoxHelper);
            this.selectedObject.debugBoxHelper = undefined;
        }

        // Réinitialisation des variables de sélection
        this.selectedObject = undefined;
        this.resetInformationsContainer();
    }

    /**
     * Affiche les informations du bot sélectionné dans le conteneur d'informations.
     * @param {Bot} bot - Le bot sélectionné.
     */
    writeBotInformations(bot) {
        // Récupération des données et création des éléments HTML
        let header = document.createElement("h1");
        header.innerHTML = `${bot.type} (${bot.modelName})`;

        let botId = document.createElement("h3");
        botId.innerHTML = `${bot.id}`;
        botId.style.color = `#${bot.teamColor?.getHexString()}`;

        let botX = document.createElement("p");
        botX.innerHTML = `X (Bot) = ${bot.x?.toFixed(3)}`;

        let botZ = document.createElement("p");
        botZ.innerHTML = `Z (Bot) = ${bot.z?.toFixed(3)}`;

        let botRy = document.createElement("p");
        botRy.innerHTML = `Ry (Bot) = ${bot.ry?.toFixed(3)}`;

        let botObjX = document.createElement("p");
        botObjX.innerHTML = `X (obj) = ${bot.sceneObject?.position.x?.toFixed(3)}`;

        let botObjZ = document.createElement("p");
        botObjZ.innerHTML = `Z (obj) = ${bot.sceneObject?.position.z?.toFixed(3)}`;

        let botObjRy = document.createElement("p");
        botObjRy.innerHTML = `Ry (obj) = ${bot.sceneObject?.rotation.y?.toFixed(3)}`;

        // Ajout des éléments HTML au conteneur d'informations
        this.infoContainer.appendChild(header);
        this.infoContainer.appendChild(document.createElement("hr"));
        this.infoContainer.appendChild(botId);
        this.infoContainer.appendChild(botX);
        this.infoContainer.appendChild(botZ);
        this.infoContainer.appendChild(botRy);
        this.infoContainer.appendChild(botObjX);
        this.infoContainer.appendChild(botObjZ);
        this.infoContainer.appendChild(botObjRy);
    }

    /**
     * Affiche les informations de l'objet sélectionné dans le conteneur d'informations.
     * @param {GameObject} object - L'objet sélectionné.
     */
    writeObjectInformations(object) {
        // Récupération des données
        let header = document.createElement("h1");
        header.innerHTML = `${object.type} (${object.modelName})`;

        let objectX = document.createElement("p");
        objectX.innerHTML = `X = ${object.x?.toFixed(3)}`;

        let objectZ = document.createElement("p");
        objectZ.innerHTML = `Z = ${object.z?.toFixed(3)}`;

        let objectRy = document.createElement("p");
        objectRy.innerHTML = `Ry = ${object.ry?.toFixed(3)}`;

        // Ajout des données au conteneur
        this.infoContainer.appendChild(header);
        this.infoContainer.appendChild(document.createElement("hr"));
        this.infoContainer.appendChild(objectX);
        this.infoContainer.appendChild(objectZ);
        this.infoContainer.appendChild(objectRy);
    }

    /**
     * Efface les informations du conteneur d'informations.
     */
    resetInformationsContainer() {
        // Clear du conteneur
        this.infoContainer.innerHTML = "";
    }
}
