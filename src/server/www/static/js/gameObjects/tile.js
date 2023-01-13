import "../actionDefinition.js"
import {actions} from "../actions/actions.js"

export default class Tile{
    constructor(construct){
        this.x = construct.x;
        this.z = construct.z;
        this.objTile = null;
        this.objObj = null;
    }

    create(tile, obj, viewController){
        viewController.createObject(this.x, 0, this.z, tile).then((objTile) => {this.objTile = objTile});
        if (obj != 'air')
            viewController.createObject(this.x, 0.5, this.z, obj).then((objObj) => {this.objObj = objObj});
    }
    
    action(key,param){
        actions[key].action.call(this, param);
    }
}