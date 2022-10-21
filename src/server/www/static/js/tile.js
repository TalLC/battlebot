import "./actionDefinition.js"

export default class Tile{
    x;
    z;
    objTile;
    objObj;

    constructor(construct){
        this.x = construct.x;
        this.z = construct.z;
        this.objTile = null;
        this.objObj = null;
    }

    async create(tile, obj, viewController){
        this.objTile = await viewController.createObject(this.x, 0, this.z, tile);
        if (obj != 'air')
            this.objObj = await viewController.createObject(this.x, 0.5, this.z, obj);
    }
}