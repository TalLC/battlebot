import logger from "../logger.js";
import GameManager from "../gameManager.js";
import Object3DFactory from "../view/object3DFactory.js";

export default class GameObject {
    /**
     * Crée un nouvel objet de jeu.
     * @param {string} id - L'identifiant de l'objet.
     * @param {string} type - Le type de l'objet.
     * @param {number} x - La position x de l'objet.
     * @param {number} y - La position y de l'objet.
     * @param {number} z - La position z de l'objet.
     * @param {number} ry - L'angle de rotation autour de l'axe y de l'objet.
     * @param {string} collisionShape - La forme de la boîte de collision de l'objet.
     * @param {number} collisionSize - La largeur ou le rayon de la boite de collision de l'objet.
     */
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

    /**
     * Supprime l'objet de la scène de jeu.
     */
    dispose() {
        // Suppression de l'objet de la scene Three.js
        GameManager().viewController.disposeSceneObject(this.sceneObject);

        // Suppression du GameObject
        // On attend un peu avant d'effacer l'entrée du dictionnaire pour éviter que le tir ne se joue après la suppression
        new Promise((resolve) => setTimeout(() => resolve(), 1000)).then(() => GameManager().removeGameObject(this));
    }

    /**
     * Renvoie les coordonnées de l'objet dans l'espace 3D.
     * @returns {object} - Les coordonnées x, y et z de l'objet.
     */
    get coordinates3D() {
        return { x: this.x, y: this.y, z: this.z };
    }

    /**
     * Renvoie les coordonnées de l'objet dans le plan xz (2D).
     * @returns {object} - Les coordonnées x et z de l'objet.
     */
    get coordinates2D() {
        return { x: this.x, z: this.z };
    }

    /**
     * Met à jour l'affichage de la boite de sélection de debug dans la scène de jeu.
     */
    render() {
        // Si on a une boxHelper, on l'update pour suivre le déplacement de l'objet
        if (this.debugBoxHelper) {
            this.debugBoxHelper.update();
        }
    }

    /**
     * Active ou désactive l'affichage de la boîte de collision de l'objet.
     */
    toggleCollisions() {
        if (this.sceneObject && this.type !== "tile") {
            if (this.collisionBox) {
                GameManager().viewController.disposeSceneObject(this.collisionBox);
                this.collisionBox = undefined;
            } else {
                this.collisionBox = Object3DFactory.createCollisionBoxForGameObject(this);
                this.sceneObject.add(this.collisionBox);
            }
        }
    }

    /**
     * Applique un nouveau matériau à l'objet.
     * @param {THREE.Material} material - Le nouveau matériau à appliquer.
     * @param {boolean} overrideMap - Si vrai, remplace aussi les textures de l'objet par le nouveau matériau.
     */
    applyMaterial(material, overrideMap) {
        logger.debug("Applying new material");
        this.sceneObject.traverse((o) => {
            if (o.isMesh && (!o.material.map || overrideMap)) {
                o.material = material;
            }
        });
    }

    /**
     * Change la couleur de l'objet.
     * @param {THREE.Color} color - La nouvelle couleur à appliquer.
     * @param {boolean} overrideMap - Si vrai, remplace aussi la texture de l'objet par de la couleur.
     */
    setColor(color, overrideMap) {
        logger.debug("Setting new color");
        this.sceneObject.traverse((o) => {
            if (o.isMesh && (!o.material.map || overrideMap)) {
                o.material.color = color;
            }
        });
    }
}
