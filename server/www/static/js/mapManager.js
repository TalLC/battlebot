import GameManager from "./gameManager.js";
import Object3DFactory from "./view/object3DFactory.js";
import MapObject from "./gameObjects/mapObject.js";
import logger from "./logger.js";

/**
 * Singleton gérant la map.
 */

let instance;

export class MapManager {
    constructor() {
        if (!instance) {
            instance = this;
            this.id;
            this.height;
            this.width;
            this.mapObjects = [];
            this.tileRotations = [-Math.PI, -Math.PI / 2, 0.0, Math.PI / 2];
        }

        return instance;
    }

    /**
     * Charge une nouvelle map dans le jeu en supprimant l'ancienne
     * @param {Object} mapData - Les données de la nouvelle map reçues depuis le serveur
     */
    loadMap(mapData) {
        this.deleteMap();

        this.id = mapData.id;
        this.height = mapData.height;
        this.width = mapData.width;
        this.createMap(mapData.tilesGrid);
    }

    /**
     * Supprime tous les MapObject et TileObject de la map
     */
    deleteMap() {
        for (let mapObject of this.mapObjects) {
            mapObject.dispose();
        }
        this.mapObjects = [];
    }

    /**
     * Renvoie une rotation aléatoire pour un MapObject ou TileObject
     * @param {Boolean} isTile - true si c'est une Tile, false si c'est un MapObject
     * @return {Number} - La rotation en radians
     */
    randomRotation(isTile) {
        if (isTile) return this.tileRotations[Math.floor(Math.random() * this.tileRotations.length)];
        else return Math.random() * 2 * Math.PI;
    }


    getRotationForMapObject(objectName) {
        let ry = 0.0;
        switch (objectName) {
            case "treesmall":
            case "treebig":
                ry = this.randomRotation(false);
                break;
            case "rock":
            case "rock2":
            case "rock3":
                ry = this.randomRotation(false);
                break;
            case "ground":
                ry = this.randomRotation(true);
                break;
            case "groundwater":
                ry = 0.0;
                break;
            case "water":
                ry = this.randomRotation(true);
                break;
            case "desintegrator":
                ry = 0.0;
                break;
            case "watermine":
                ry = this.randomRotation(false);
                break;      
            default:
                ry = 0.0;
        }
        return ry;
    }

    /**
     * Ajoute un MapObject au jeu
     * @param {Object} mapObjectData - Les données du MapObject
     */
    addMapObject(mapObjectData) {
        this.mapObjects[mapObjectData.id] = new MapObject(
            mapObjectData.id,
            mapObjectData.type,
            mapObjectData.x,
            mapObjectData.y,
            mapObjectData.z,
            mapObjectData.ry,
            mapObjectData.collisionShape,
            mapObjectData.collisionSize,
            mapObjectData.model
        );
        if (mapObjectData.model !== "air") {
            console.log(mapObjectData.model);
            console.log(mapObjectData.id);
            Object3DFactory.createMapObject3D(this.mapObjects[mapObjectData.id]).then((sceneObject) => {
                GameManager().viewController.scene.add(sceneObject);
            });
        }
    }

    /**
     * Crée la map en appelant addMapObject pour chaque Tile et TileObject
     * @param {Array} tilesGrid - La grille de tuiles avec leurs objets associés
     */
    createMap(tilesGrid) {
        for (let tile of tilesGrid) {
            // Ajout de la Tile
            this.addMapObject({
                id: tile.id,
                type: "tile",
                x: tile.x,
                y: 0.0,
                z: tile.z,
                ry: this.getRotationForMapObject(tile.name.toLowerCase()),
                collisionShape: tile.shape_name.toLowerCase(),
                collisionSize: tile.shape_size,
                model: tile.name.toLowerCase()
            });
            
            // Ajout du TileObject si présent
            if (tile.object) {
                this.addMapObject({
                    id: tile.object.id,
                    type: "tileObject",
                    x: tile.object.x,
                    y: 0.5,
                    z: tile.object.z,
                    ry: this.getRotationForMapObject(tile.object.name.toLowerCase()),
                    collisionShape: tile.object.shape_name.toLowerCase(),
                    collisionSize: tile.object.shape_size,
                    model: tile.object.name.toLowerCase()
                });
            }
        }
    }
}

export default new MapManager();
