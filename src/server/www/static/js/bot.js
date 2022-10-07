import "./actionDefinition.js"
import {actions} from "./actions/actions.js"

export default class Bot
{
    id;
    x;
    z;
    ry;
    shoot;
    hit;
    shield_hide;
    shield_raise;

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
    }
    
    action(key,param){
        console.log(param)
        actions[key].action.call(this, param);
    }
}