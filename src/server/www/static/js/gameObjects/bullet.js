import GameObject from './gameObject.js'
import TWEEN from 'tween';

export default class Bullet extends GameObject {
    /**
     * Crée un nouvelle bullet en jeu.
     * @param {number} x - La position x de l'objet.
     * @param {number} y - La position y de l'objet.
     * @param {number} z - La position z de l'objet.
     * @param {number} ry - L'angle de rotation autour de l'axe y de l'objet.
     * @param {string} teamColor - La couleur de l'équipe du bot sous forme de chaîne hexadécimale. 
     */
    constructor(x, y, z, ry, teamColor) {
        super(null, "bullet", x, y, z, ry, null, null);
        this.sceneObject;
        this.teamColor = teamColor;
        this.x = x;
        this.y = y;
        this.z = z;
        this.ry = ry;
    }

    /**
     * Permet le deplacement de la bullet.
     * @param {dict} target - La position de la cible.
     */
    moveTo(target){
        new TWEEN.Tween({x: this.sceneObject.position.x , z: this.sceneObject.position.z})
            .to({x: target.x , z: target.z}, 100)
            .easing(TWEEN.Easing.Linear.None)
            .onUpdate((coords) => {
                this.sceneObject.position.x = coords.x;
                this.sceneObject.position.z = coords.z;
                if (this.sceneObject.position.x === target.x && this.sceneObject.position.z === target.z){
                    this.dispose();
                }
            })
            .start()
    }
}