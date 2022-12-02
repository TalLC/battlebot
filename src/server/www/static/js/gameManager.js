import View3DController from "./view/view3DController.js";
import bot from "./bot.js"
import tile from "./tile.js"

class GameManager{
    v = new View3DController();
    bots = {};
    map = [];

    constructor(){
        let map;
        let bots;
        let v;
    }

    /*  
        Fonction : Permet la création d'une classe bot et de l'appel à la fonction de création du Bot.
        Param : id -> ID unique du Bot
                x -> Position en x du Bot
                z -> Position en z du Bot
                ry -> Rotation autour de l'axe y du Bot
        Return : N/A
    */
    createBot(id, x, z, ry){
        this.bots[id] = new bot({id:id, x:x, z:z, ry:ry, avatar:'./static/models/robot_1.glb'});
        this.bots[id].create(this.v);
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
                for (let tileR in mapData['tiles'])
                 {
                    tileR = mapData['tiles'][tileR];
                    if (h === tileR['x'] && w === tileR['z']){
                        var tmpTile = new tile({x:h, z:w});
                        tmpTile.create(tileR['tile'], tileR['tile_object'], this.v);
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