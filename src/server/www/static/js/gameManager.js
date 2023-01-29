import View3DController from "./view/view3DController.js";
import Object3DFactory from "./view/object3DFactory.js";
import Bot from "./gameObjects/bot.js"
import MapObject from "./gameObjects/mapObject.js"
import {getRandomInt} from "./utils.js"


class GameManager {
    constructor(){
        this.v = new View3DController("view-container");
        this.loginId;
        this.bots = {};
        this.mapObjects = {};
    }

    render() {
        for (let bot of Object.values(this.bots)) {
            bot.render();
        }

        this.v.render();
    }

    start() {
        // Masquer la page d'attente
        const startgameContainer = document.getElementById("startgame-container");
        startgameContainer.hidden = true;

        this.v.start();
    }

    /*
        Fonction : Permet la création de Bots dans le jeu.
        Param : bot_id -> ID unique du Bot
                x -> Position en x
                z -> Position en z
                ry -> Rotation autour de l'axe y
                team_color -> Couleur de l'équipe à laquelle appartient le Bot
                model_name -> Nom du modèle 3D représentant le bot
        Return : N/A
    */
    addBot(botData) {
        this.bots[botData.id] = new Bot(
            botData.id,
            botData.x, botData.z, -1 * botData.ry,
            botData.team_color,
            botData.shape_name.toLowerCase(),
            botData.shape_size,
            botData.model_name
        );
        console.log(this.bots[botData.id]);
        Object3DFactory.createBot3D(this.bots[botData.id]).then(sceneObject => {
            this.v.scene.add(sceneObject);
        });
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
                this.v.scene.add(sceneObject);
            });
        }
    }

    /*
        Fonction : Retrouve un GameObject à partir d'un objet de la scène ThreeJs.
        Param : sceneObject -> Objet de la scène ThreeJs
                checkFor -> Type de GameObject à trouver
        Return : GameObject
    */
    getGameObjectFromSceneObject(sceneObject, checkFor) {
        if (checkFor === "bot") {
            for(let obj of Object.values(this.bots)) {
                if (obj.type === "bot" && obj.sceneObject === sceneObject) {
                    return obj;
                }
            }
        } else if (checkFor === "tileObject" || checkFor === "tile") {
            for(let obj of Object.values(this.mapObjects)) {
                if (obj.sceneObject) {
                    if (obj.type === checkFor) {
                        if (obj.sceneObject === sceneObject) {
                            return obj;
                        }
                        if (obj.sceneObject === sceneObject.parent) {
                            return obj;
                        }
                    }
                }
            }
        }
    }

    /*
        Fonction : Permet la création/stockage dans une liste de la MAP en appelant la fonction de création d'objet pour chaque tuile/objet.
        Param : mapData -> Les données de la MAP reçu depuis le back avec toute les tuiles/objets.
        Return : N/A
    */
    createMap(mapData) {
        for (let h = 0; h < mapData.height; h++)
        {
            for (let w = 0; w < mapData.width; w++)
            {
                for (let tile in mapData['tiles_grid'])
                 {
                    tile = mapData['tiles_grid'][tile];
                    if (h === tile['x'] && w === tile['z']) {
                        
                        // Ajout de la Tile
                        this.addMapObject(
                            {
                                id: tile['id'],
                                type: 'tile',
                                x: tile['x'],
                                y: 0.0,
                                z: tile['z'],
                                ry: 0.0,
                                collisionShape: tile['shape_name'],
                                collisionSize: tile['shape_size'],
                                model: tile['name'].toLowerCase()
                            }
                        );
                        
                        // Ajout du TileObject si présent
                        if (tile.object) {
                            const ry = getRandomInt(Math.floor(2 * Math.PI * 100)) / 100
                            this.addMapObject(
                                {
                                    id: tile['object']['id'],
                                    type: 'tileObject',
                                    x: tile['object']['x'],
                                    y: 0.5,
                                    z: tile['object']['z'],
                                    ry: ry,
                                    collisionShape: tile['object']['shape_name'],
                                    collisionSize: tile['object']['shape_size'],
                                    model: tile['object']['name'].toLowerCase()
                                }
                            );
                        }

                        break;
                    }
                }
            }
        }
    }

}

export default new GameManager();
