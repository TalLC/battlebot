import * as THREE from "three";
import logger from "../logger.js";
import { GLTFLoader } from "loaders/GLTFLoader";
import graphicObjects from "./graphicObjects.js";

/**
 * Singleton gérant la création des objets 3D.
 */

let instance;

export class Object3DFactory {
    constructor() {
        if (!instance) {
            instance = this;
            this.loader = new GLTFLoader();

            // Cache des modèles 3D déjà chargés
            this.loadedModels = {};

            // Constitution du cache
            this.caching = this.preloadModels();
        }

        return instance;
    }

    /**
     * Charge un modèle 3D ou retourne une référence si déjà chargé.
     * @param {string} modelPath - Chemin du fichier du modèle 3D.
     * @returns {Promise<THREE.Group>} - Une promesse qui retourne l'objet 3D.
     */
    loadModel(modelPath) {
        if (this.loadedModels[modelPath]) {
            // Si le modèle a déjà été chargé, retourne la référence à l'objet Group du modèle
            return Promise.resolve(this.loadedModels[modelPath].clone());
        } else {
            // Sinon, charge le modèle en utilisant GLTFLoader et stocke la référence à l'objet Group du modèle dans le dictionnaire
            return new Promise((resolve, reject) => {
                this.loader.load(
                    modelPath,
                    (gltf) => {
                        // Conversion du material Basic en Phong
                        gltf.scene.traverse((o) => {
                            if (o.isMesh) {
                                let prevMaterial = o.material;
                                o.material = new THREE.MeshPhongMaterial();
                                THREE.MeshBasicMaterial.prototype.copy.call(o.material, prevMaterial);
                                o.receiveShadow = true;
                                o.castShadow = true;
                            }
                        });

                        // Stockage de la référence vers le modèle 3D
                        this.loadedModels[modelPath] = gltf.scene;

                        const gltfInstance = this.loadedModels[modelPath].clone();
                        resolve(gltfInstance);
                    },
                    undefined,
                    function (error) {
                        console.error(`Erreur lors du chargement du modèle ${modelPath}`, error);
                        reject(error);
                    }
                );
            });
        }
    }

    /**
     * Précharge les modèles 3D pour les stocker en cache.
     * @returns {Promise<void>} - Une promesse qui se résout lorsque tous les modèles sont chargés.
     */
    preloadModels() {
        let loadModelPromises = [];
        for (let modelPath of Object.values(graphicObjects)) {
            if (typeof modelPath === "object" && modelPath !== null) {
                for (let subModelPath of Object.values(modelPath)) {
                    loadModelPromises.push(this.loadModel(subModelPath));
                }
            } else {
                loadModelPromises.push(this.loadModel(modelPath));
            }
        }

        logger.debug(`Mise en cache de ${loadModelPromises.length} modèles 3D...`);

        return Promise.all(loadModelPromises).then(() => {
            logger.debug("Cache 3D généré !");
        });
    }

    /**
     * Crée un objet 3D et définit sa position et sa rotation.
     * @param {number} x - Position en x de l'objet.
     * @param {number} y - Position en y de l'objet.
     * @param {number} z - Position en z de l'objet.
     * @param {number} ry - Rotation en y de l'objet.
     * @param {string} modelPath - Chemin du fichier 3D à charger.
     * @returns {Promise<THREE.Object3D>} - Une promesse qui retourne l'objet de la scène.
     */
    createObject(x, y, z, ry, modelPath) {
        return this.loadModel(modelPath).then((sceneObject) => {
            sceneObject.position.x = x;
            sceneObject.position.y = y;
            sceneObject.position.z = z;
            sceneObject.rotation.y = ry;
            return sceneObject;
        });
    }

    /**
     * Crée un objet 3D pour un bot.
     * @param {Object} bot - L'objet Bot dont on veut créer le modèle 3D.
     * @returns {Promise<THREE.Object3D>} - Une promesse qui retourne le modèle 3D du bot.
     */
    createBot3D(bot) {
        const modelPath = bot.modelName === undefined ? graphicObjects["avatar"]["default"] : graphicObjects["avatar"][bot.modelName];
        return this.createObject(bot.x, bot.y, bot.z, bot.ry, modelPath).then((sceneObject) => {
            // Clonage du material car chaque Bot doit avoir son propre material
            sceneObject.traverse((o) => {
                if (o.isMesh) o.material = o.material.clone();
            });

            // Assignation du modèle 3D au Bot
            bot.sceneObject = sceneObject;
            
            // On peint le Bot de la couleur de l'équipe
            bot.setColor(new THREE.Color(bot.teamColor).add(new THREE.Color(0x323232)), false);

            return sceneObject;
        });
    }

    /**
     * Crée un objet 3D pour un objet de carte (mapObject).
     * @param {Object} mapObject - L'objet MapObject dont on veut créer le modèle 3D.
     * @returns {Promise<THREE.Object3D>} - Une promesse qui retourne le modèle 3D de l'objet de carte.
     */
    createMapObject3D(mapObject) {
        const modelPath = graphicObjects[mapObject.modelName];
        if (modelPath) {
            return this.createObject(mapObject.x, mapObject.y, mapObject.z, mapObject.ry, modelPath).then((sceneObject) => {
                mapObject.sceneObject = sceneObject;
                return sceneObject;
            });
        }
    }

    /**
     * Crée un maillage pour un faisceau laser.
     * @param {THREE.Color} color - Couleur du laser.
     * @param {Array<number>} startArray - Position de départ du laser.
     * @param {Array<number>} endArray - Position de fin du laser.
     * @returns {THREE.Mesh} - Le maillage du laser.
     */
    createLaserMesh(color, startArray, endArray) {
        const start = new THREE.Vector3(...startArray);
        const end = new THREE.Vector3(...endArray);

        // Create a material
        const material = new THREE.MeshBasicMaterial({ color: color });

        // edge from X to Y
        var direction = new THREE.Vector3().subVectors(end, start);

        // Make the geometry (of "direction" length)
        var geometry = new THREE.CylinderGeometry(0.07, 0.1, direction.length(), 6, 4, false);

        // shift it so one end rests on the origin
        geometry.applyMatrix4(new THREE.Matrix4().makeTranslation(0, direction.length() / 2, 0));

        // rotate it the right way for lookAt to work
        geometry.applyMatrix4(new THREE.Matrix4().makeRotationX(THREE.MathUtils.degToRad(90)));

        // Make a mesh with the geometry
        var cylinderMesh = new THREE.Mesh(geometry, material);

        // Position it where we want
        cylinderMesh.position.copy(start);

        // And make it point to where we want
        cylinderMesh.lookAt(end);

        return cylinderMesh;
    }

    /**
     * Crée une boîte de collision pour un objet de jeu (gameObject).
     * @param {Object} gameObject - L'objet de jeu pour lequel créer la boîte de collision.
     * @returns {THREE.Mesh} - Le maillage de la boîte de collision.
     */
    createCollisionBoxForGameObject(gameObject) {
        const objectBox = new THREE.Box3().setFromObject(gameObject.sceneObject);
        const size = new THREE.Vector3();
        objectBox.getSize(size);
        const height = size.y;        
        const color = gameObject.type === 'bot' ? gameObject.teamColor : 0xffff00;

        let geometry;
        if (gameObject.collisionShape === "circle") {
            geometry = new THREE.CylinderGeometry(gameObject.collisionSize, gameObject.collisionSize, height, 8);
        } else {
            geometry = new THREE.BoxGeometry(gameObject.collisionSize, height);
        }

        const material = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.5
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.y += height / 2;
        mesh.rotation.y = gameObject.ry;
        return mesh;
    }
}

export default new Object3DFactory();
