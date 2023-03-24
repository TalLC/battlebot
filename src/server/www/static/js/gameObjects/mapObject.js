import GameObject from "./gameObject.js";

export default class MapObject extends GameObject {
    /**
     * Crée un objet de la carte.
     * @param {String} id - Identifiant de l'objet.
     * @param {String} type - Type d'objet.
     * @param {Number} x - Position x de l'objet.
     * @param {Number} y - Position y de l'objet.
     * @param {Number} z - Position z de l'objet.
     * @param {Number} ry - Rotation y de l'objet.
     * @param {String} collisionShape - Forme de la collision.
     * @param {Number} collisionSize - Taille de la collision.
     * @param {String} modelName - Nom du modèle de l'objet.
     */
    constructor(id, type, x, y, z, ry, collisionShape, collisionSize, modelName) {
        super(id, type, x, y, z, ry, collisionShape, collisionSize);
        this.modelName = modelName;
        this.sceneObject = null;
    }
}
