import View3DController from "./view/view3DController.js";
import bot from "./bot.js"

class GameManager{
    v = new View3DController();
    bots = {};

    constructor(){
        //map = new GameMap();
        let bots;
        let v;
    }

    async createBot(id, x, z, ry){
        this.bots[id] = new bot({id:id, x:x, z:z, ry:ry, avatar:'./static/models/robot_1.glb'}, this.v);
        await this.bots[id].create(this.v)
    }
}

export default new GameManager();

//b.action('move', {x:5, z:5});