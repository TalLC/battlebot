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

    async createBot(id, x, z, ry){
        this.bots[id] = new bot({id:id, x:x, z:z, ry:ry, avatar:'./static/models/robot_1.glb'});
        await this.bots[id].create(this.v);
    }

    async createMap(mapData){
        for (let h = 0; h < mapData.height; h++)
        {
            let current_line = [];
            for (let w = 0; w < mapData.width; w++)
            {
                for (let tileR in mapData['tiles'])
                 {
                    tileR = mapData['tiles'][tileR];
                    if (h === tileR['x'] && w === tileR['z']){
                        console.log(tileR['x'])
                        var tmpTile = new tile({x:h, z:w});
                        await tmpTile.create(tileR['tile'], tileR['tile_object'], this.v)
                        console.log(tmpTile)
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