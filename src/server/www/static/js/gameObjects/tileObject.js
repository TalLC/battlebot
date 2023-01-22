import GameObject from './gameObject.js';


export default class TileObject extends GameObject{
    constructor(construct){

        // Rotation forcée ou aléatoire pour les objets placés
        let ry;
        if (construct.ry) {
            ry = construct.ry;
        } else {
            ry = Math.random();
        }
        
        super(construct.id, "tileObject", construct.x, construct.z, ry);
    }
}
