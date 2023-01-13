import View3DController from "./view/view3DController.js";
import bot from "./gameObjects/bot.js"
import tile from "./gameObjects/tile.js"

class GameManager{
    v = new View3DController();
    bots = {};
    map = [];
    mapObjects = {};

    constructor(){
        let map;
        let bots;
        let v;
        let mapObjects;
    }

    createBot(id, x, z, ry){
        this.bots[id] = new bot({id:id, x:x, z:z, ry:ry, avatar:'./static/models/robot_1.glb'});
        this.bots[id].create(this.v);
    }

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
                        console.log("h", h, "w", w);


                        var tmpTile = new tile({x:h, z:w});
                        console.log("tmpTile", tmpTile);

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