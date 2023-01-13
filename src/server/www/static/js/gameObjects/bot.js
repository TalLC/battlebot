import "../actionDefinition.js"
import {actions} from "../actions/actions.js"

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
    enrolled;

    constructor(construct){
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
        this.enrolled = false;
    }

    create(viewController){
        viewController.createBot(this.x, this.ry, this.z, 'avatar', 0).then((objBot) => {this.objBot = objBot});
    }
    
    action(key,param){
        actions[key].action.call(this, param);
    }
}