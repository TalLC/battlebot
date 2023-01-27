import View3DController from "./view/view3DController.js";
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

    /*
        Fonction : Permet la création de Bots dans le jeu.
        Param : id -> ID unique du Bot
                x -> Position en x
                z -> Position en z
                ry -> Rotation autour de l'axe y
                teamColor -> Couleur de l'équipe à laquelle appartient le Bot
                modelName -> Nom du modèle 3D représentant le bot
        Return : N/A
    */
    addBot(id, x, z, ry, teamColor, modelName="default") {
        this.bots[id] = new Bot({id:id, x:x, z:z, ry:ry, teamColor:teamColor, modelName:modelName});
        this.v.createBot3D(this.bots[id]);
    }

    /*
        Fonction : Permet la création d'un Map objects dans le jeu.
        Param : id -> ID unique de l'objet
                x -> Position en x
                y -> Position en y
                z -> Position en z
                ry -> Rotation autour de l'axe y
                modelName -> Nom du modèle 3D représentant l'objet
        Return : N/A
    */
    addMapObject(id, type, x, y, z, ry, modelName=null) {
        this.mapObjects[id] = new MapObject({id:id, type:type, x:x, y:y, z:z, ry:ry, modelName:modelName});
        if (modelName !== "air") {
            this.v.createMapObject3D(this.mapObjects[id]);
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
                        this.addMapObject(tile['id'], 'tile', tile['x'], 0.0, tile['z'], 0.0, tile['name'].toLowerCase());
                        
                        // Ajout du TileObject si présent
                        if (tile.object) {
                            const ry = getRandomInt(Math.floor(2 * Math.PI * 100)) / 100
                            this.addMapObject(tile['object']['id'], 'tileObject', tile['object']['x'], 0.5, tile['object']['z'], ry, tile['object']['name'].toLowerCase());
                        }

                        break;
                    }
                }
            }
        }
    }

}

export default new GameManager();
