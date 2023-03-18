import GameManager from './gameManager.js';
import Object3DFactory from "./view/object3DFactory.js";
import MapObject from "./gameObjects/mapObject.js"
import { getRandomInt } from "./utils/utils.js"


let instance;

export class MapManager {
    constructor() {
        if (!instance) {
            instance = this;
            this.id;
            this.height;
            this.width;
            this.mapObjects = [];
            this.tileRotations = [-Math.PI, -Math.PI/2, 0.0, Math.PI/2]
        }

        return instance;
    }

    loadMap(mapData) {
        this.deleteMap();

        this.id = mapData.id;
        this.height = mapData.height;
        this.width = mapData.width;
        this.createMap(mapData.tilesGrid)
    }

    deleteMap() {
        for (let mapObject of this.mapObjects) {
            mapObject.dispose();
        }
        this.mapObjects = [];
    }

    randomRotation(isTile) {
        if (isTile) return this.tileRotations[Math.floor(Math.random() * this.tileRotations.length)];
        else return getRandomInt(Math.floor(2 * Math.PI * 100)) / 100;
    }

    /*
        Fonction : Permet la création d'un Map objects dans le jeu.
        Param : id -> ID unique de l'objet
                type -> Type d'objet
                x -> Position en x
                y -> Position en y
                z -> Position en z
                ry -> Rotation autour de l'axe y
                model -> Nom du modèle 3D représentant l'objet
        Return : N/A
    */
    addMapObject(mapObjectData) {
        this.mapObjects[mapObjectData.id] = new MapObject(
            mapObjectData.id,
            mapObjectData.type,
            mapObjectData.x, mapObjectData.y, mapObjectData.z, mapObjectData.ry,
            mapObjectData.collisionShape, mapObjectData.collisionSize,
            mapObjectData.model
        );
        if (mapObjectData.model !== "air") {
            Object3DFactory.createMapObject3D(this.mapObjects[mapObjectData.id]).then(sceneObject => {
                GameManager().viewController.scene.add(sceneObject);
            });
        }
    }


    /*
        Fonction : Permet la création/stockage dans une liste de la MAP en appelant la fonction de création d'objet pour chaque tuile/objet.
        Param : mapData -> Les données de la MAP reçu depuis le back avec toute les tuiles/objets.
        Return : N/A
    */
    createMap(tilesGrid) {
        for (let tile of tilesGrid) {
           // Ajout de la Tile
           this.addMapObject(
               {
                   id: tile['id'],
                   type: 'tile',
                   x: tile['x'],
                   y: 0.0,
                   z: tile['z'],
                   ry: this.randomRotation(true),
                   collisionShape: tile['shape_name'].toLowerCase(),
                   collisionSize: tile['shape_size'],
                   model: tile['name'].toLowerCase()
               }
           );
           
           // Ajout du TileObject si présent
           if (tile.object) {
               this.addMapObject(
                   {
                       id: tile['object']['id'],
                       type: 'tileObject',
                       x: tile['object']['x'],
                       y: 0.5,
                       z: tile['object']['z'],
                       ry: this.randomRotation(false),
                       collisionShape: tile['object']['shape_name'].toLowerCase(),
                       collisionSize: tile['object']['shape_size'],
                       model: tile['object']['name'].toLowerCase()
                   }
               );
           }
       }
    }

}

export default new MapManager();
