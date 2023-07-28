import logger from "../logger.js";
import * as THREE from "three";
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
        this._sceneObject;
        this._x = x;
        this._y = y;
        this._z = z;
        this._ry = ry;
        this.collisionShape = collisionShape;
        this.collisionSize = collisionSize;
        this.collisionBox;
        this.debugBoxHelper;
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.5, 10);
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
     * Obtient la position x de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, retourne la valeur stockée dans la variable _x.
     * @type {number}
     */
    get x() {
        if (this.sceneObject) return this.sceneObject.position.x;
        else return this._x;
    }

    /**
     * Définit la position x de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, stocke la valeur dans la variable _x.
     * @type {number}
     */
    set x(newValue) {
        if (this.sceneObject) this.sceneObject.position.x = newValue;
        if (this.camera) this.camera.position.x = newValue;
        this._x = newValue;
    }

    /**
     * Obtient la position y de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, retourne la valeur stockée dans la variable _y.
     * @type {number}
     */
    get y() {
        if (this.sceneObject) return this.sceneObject.position.y;
        else return this._y;
    }

    /**
     * Définit la position y de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, stocke la valeur dans la variable _y.
     * @type {number}
     */
    set y(newValue) {
        if (this.sceneObject) this.sceneObject.position.y = newValue;
        if (this.camera) this.camera.position.y = newValue + 1.5;
        this._y = newValue;
    }

    /**
     * Obtient la position z de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, retourne la valeur stockée dans la variable _z.
     * @type {number}
     */
    get z() {
        if (this.sceneObject) return this.sceneObject.position.z;
        else return this._z;
    }

    /**
     * Définit la position z de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, stocke la valeur dans la variable _z.
     * @type {number}
     */
    set z(newValue) {
        if (this.sceneObject) this.sceneObject.position.z = newValue;
        if (this.camera) this.camera.position.z = newValue;
        this._z = newValue;
    }

    /**
     * Obtient la rotation y de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, retourne la valeur stockée dans la variable _ry.
     * @type {number}
     */
    get ry() {
        if (this.sceneObject) return this.sceneObject.rotation.y;
        else return this._ry;
    }

    /**
     * Définit la rotation y de l'objet dans la scène. Si l'objet n'a pas encore été ajouté à la scène, stocke la valeur dans la variable _ry.
     * @type {number}
     */
    set ry(newValue) {
        if (this.sceneObject) this.sceneObject.rotation.y = newValue;
        if (this.camera) this.camera.rotation.y = newValue + (-1 * Math.PI) / 2;
        this._ry = newValue;
    }

    /**
     * Définit l'objet dans la scène en positionnant sa position x, y, z et sa rotation y si les variables sont définies.
     * @type {THREE.Object3D}
     */
    set sceneObject(newValue) {
        if (newValue) {
            newValue.position.x = this._x;
            this.camera.position.x = this._x;
            newValue.position.y = this._y;
            this.camera.position.y = this._y + 1.5;
            newValue.position.z = this._z;
            this.camera.position.z = this._z;
            newValue.rotation.y = this._ry;
            this.camera.rotation.y = this._ry + (-1 * Math.PI) / 2;
        }
        this._sceneObject = newValue;
    }

    /**
     * Obtient l'objet dans la scène.
     * @type {number}
     */
    get sceneObject() {
        return this._sceneObject;
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
