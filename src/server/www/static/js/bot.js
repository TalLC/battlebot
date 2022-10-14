import "./actionDefinition.js"
import {actions} from "./actions/actions.js"

export default class Bot{
    id;
    x;
    z;
    ry;
    shoot;
    hit;
    shieldHide;
    shieldRaise;
    objBot;

    constructor(construct, viewController){
        this.id = construct.id;
        this.x = construct.x;
        this.z = construct.z;
        this.ry = construct.ry;
        this.shoot = false;
        this.hit = false;
        this.shieldHide = false;
        this.shieldRaise = false;
        this.avatarPath = construct.avatar;
        this.objBot = null;
    }

    async create(viewController){
        this.objBot = await viewController.createBot(this.x, this.ry, this.z, 'avatar', 0);
    }
    
    action(key,param){
        actions[key].action.call(this, param);
    }
}