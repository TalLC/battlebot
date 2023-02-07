import GameManager from "../gameManager.js";
import Object3DFactory from "../view/object3DFactory.js";


export default class GameObject{
    constructor(id, type, x, y, z, ry, collisionShape, collisionSize) {
        this.id = id;
        this.type = type;
        this.sceneObject;
        this.x = x;
        this.y = y;
        this.z = z;
        this.ry = ry;
        this.collisionShape = collisionShape;
        this.collisionSize = collisionSize;
        this.collisionBox;
        this.debugBoxHelper;
    }

    dispose() {
        // Suppression de l'objet de la scene Three.js
        GameManager.v.disposeSceneObject(this.sceneObject);

        // Suppression du Gameobject
        // On attend un peu avant d'effacer l'entrée du dictionnaire pour éviter que le tir ne se joue après la suppression
        new Promise((resolve) => setTimeout(() => resolve(), 1000))
            .then(() => GameManager.removeGameObject(this));
    }

    get coordinates3D() {
        return {x: this.x, z: this.z};
    }

    get coordinates2D() {
        return {x: this.x, z: this.z};
    }

    render() {
        // Si on a une boxHelper, on l'update pour suivre le déplacement de l'objet
        if (this.debugBoxHelper) {
            this.debugBoxHelper.update();
        }
    }

    toggleCollisions() {
        if (this.sceneObject && this.type !== "tile") {
            if (this.collisionBox) {
                GameManager.v.disposeSceneObject( this.collisionBox );
                this.collisionBox = undefined;
            } else {
                this.collisionBox = Object3DFactory.createCollisionBoxForGameObject(this);
                this.sceneObject.add( this.collisionBox );
            }
        }
    }
}
