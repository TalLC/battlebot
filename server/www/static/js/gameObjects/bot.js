import "../actions/botActions/botActionDefinition.js";
import { actions } from "../actions/actions.js";
import GameObject from "./gameObject.js";
import { colorStrToNumber } from "../utils/utils.js";
import * as THREE from "three";

export default class Bot extends GameObject {
    /**
     * Crée une instance de Bot.
     * @param {number} id - L'ID du bot.
     * @param {number} x - La coordonnée X du bot.
     * @param {number} z - La coordonnée Z du bot.
     * @param {number} ry - L'angle de rotation en Y du bot.
     * @param {string} teamColor - La couleur de l'équipe du bot sous forme de chaîne hexadécimale.
     * @param {string} collisionShape - La forme de la boîte de collision.
     * @param {number} collisionSize - La taille de la boîte de collision.
     * @param {string} modelName - Le nom du modèle de bot.
     */
    constructor(id, x, z, ry, teamColor, collisionShape, collisionSize, modelName) {
        super(id, "bot", x, 0.5, z, ry, collisionShape, collisionSize);
        this.teamColor = colorStrToNumber(teamColor);
        this.modelName = modelName;
        this.sceneObject = null;
        this.shoot = false;
        this.hit = false;
        this.shieldHide = false;
        this.shieldRaise = false;
        this.enrolled = false;
        this.bullet = null;
    }
    
    /**
     * Permet l'appel à une action interagissant avec le bot (actions définies dans botActionDefinition.js)
     * @param {String} key - Nom de l'action.
     * @param {Object} param - Paramètres de l'action.
     */
    action(key, param) {
        actions[key].action.call(this, param);
    }

    /**
     * Applique un nouveau matériau partiellement transparent.
     */
    kill() {
        this.applyMaterial(
            new THREE.MeshPhongMaterial({
                color: 0x424242,
                transparent: true,
                opacity: 0.7
            }),
            true
        );
    }

    /**
     * Affiche le champs de vision du bot.
     */
    showFov() {
        // Affichage du cône de vision
        const triangleGeometry = new THREE.BufferGeometry();
        const vertices = new Float32Array([
            0, 0, 0,
            10, 0, -10,
            -10, 0, -10
        ]);
        triangleGeometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    
        const triangleMaterial = new THREE.LineBasicMaterial({ color: this.teamColor });
        let triangleMesh = new THREE.LineLoop(triangleGeometry, triangleMaterial);
        triangleMesh.position.y = 1.0;
        triangleMesh.rotation.y = -Math.PI / 2;

        this.sceneObject.add(triangleMesh);
    }
}
