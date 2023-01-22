import View3DController from "./view/view3DController.js";
import bot from "./gameObjects/bot.js"
import tile from "./gameObjects/tile.js"


class GameManager{
    constructor(){
        this.v = new View3DController("view-container");
        this.bots = {};
        this.map = [];
        this.mapObjects = {};
    }

    /*
        Fonction : Permet la création d'une classe bot et de l'appel à la fonction de création du Bot.
        Param : id -> ID unique du Bot
                x -> Position en x du Bot
                z -> Position en z du Bot
                ry -> Rotation autour de l'axe y du Bot
        Return : N/A
    */
    createBot(id, x, z, ry, teamColor){
        this.bots[id] = new bot({id:id, x:x, z:z, ry:ry, teamColor:teamColor, avatar:'./static/models/robot_1.glb'});
        this.bots[id].create(this.v);
    }

    getObjectFromSceneObject(sceneObject, checkFor) {
        if (checkFor === "bot") {
            for(let bot of Object.values(this.bots)) {
                if (bot.objBot.children[0] === sceneObject) {
                    return bot;
                }
            }
        } else if (checkFor === "tile") {
            for(let obj of Object.values(this.mapObjects)) {
                if (obj.objTile === sceneObject) {
                    return obj;
                }
            }
        } else if (checkFor === "tileObject") {
            for(let obj of Object.values(this.mapObjects)) {
                if (obj.objObj === sceneObject) {
                    return obj;
                }
            }
        }
    }

    /*
        Fonction : Permet la création/stockage dans une liste de la MAP en appelant la fonction de création d'objet pour chaque tuile/objet.
        Param : mapData -> Les données de la MAP reçu depuis le back avec toute les tuiles/objets.
        Return : N/A
    */
    createMap(mapData){
        for (let h = 0; h < mapData.height; h++)
        {
            let current_line = [];
            for (let w = 0; w < mapData.width; w++)
            {
                for (let tileR in mapData['tiles_grid'])
                 {
                    tileR = mapData['tiles_grid'][tileR];
                    if (h === tileR['x'] && w === tileR['z']){
                        var tmpTile = new tile({x:h, z:w});
                        tmpTile.create(tileR['name'].toLowerCase(), tileR['object']['name'].toLowerCase(), this.v);
                        this.mapObjects[tileR['id']] = tmpTile;
                        current_line.push(tmpTile);
                        break;
                    }
                }
            }
            this.map.push(current_line);
        }
    }

}

export default new GameManager();
