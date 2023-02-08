import * as THREE from 'three';
import {GLTFLoader} from 'loaders/GLTFLoader';
import graphicObjects from "./graphicObjects.js";


class Object3DFactory {
    constructor() {
        this.loader = new GLTFLoader();
    }


    /*
        Fonction : Permet la création d'une Promise qui sera utilisé pour la création des Objets 3D.
        Param : obj -> Nom de l'objet à ajouter à la scene.
        Return :  Une Promise qui servira à la création et ajout à la scène des Objets 3D
    */
    modelLoader(obj) {
        return new Promise((resolve, reject) => {
            this.loader.load(obj, data=> resolve(data), null, reject);
        });
    }

    /*
        Fonction : Permet la création/ajout à la scène d'un objet. Est appelé à chaque nouvel objet (Arbre, Mur, Rocher, Sol, Eau...).
        Param : x -> Position en x de l'objet
                y -> Position en y de l'objet
                z -> Position en z de l'objet
                ry -> Rotation en y de l'objet
                modelPath -> Chemin du fichier 3D à charger
        Return :  Une Promise qui retournera à terme l'objet de la scene afin de pouvoir intéragir avec en cas de destruction par exemple.
    */
    createObject(x, y, z, ry, modelPath) {
        return this.modelLoader(modelPath).then(
            (gltfData) => {
                gltfData.scene.position.x = x;
                gltfData.scene.position.y = y;
                gltfData.scene.position.z = z;
                gltfData.scene.rotation.y = ry;
                gltfData.scene.receiveShadow = true;
                gltfData.scene.castShadow = true;
                return(gltfData.scene);
            }
        );
    }

    /*
        Fonction : Permet la création/ajout d'un objet Bot à la scène.
        Param : bot -> L'objet Bot dont on veut créer le modèle 3D
        Return : Une Promise qui retournera à terme le modèle 3D afin de pouvoir intéragir avec.
    */
    createBot3D(bot) {
        const modelPath = bot.modelName === undefined? graphicObjects['avatar']['default'] : graphicObjects['avatar'][bot.modelName];
        return this.createObject(bot.x, bot.y, bot.z, bot.ry, modelPath).then(sceneObject => {
            // Peinture du bot de la couleur de l'équipe
            const material = new THREE.MeshBasicMaterial({ "color": bot.teamColor });

            sceneObject.traverse((o) => {
                if (o.isMesh) o.material = material;
            });

            bot.sceneObject = sceneObject;
            return sceneObject;
        });
    }

    /*
        Fonction : Permet la création/ajout d'un objet 3D à la scène (tile, tile object, ...).
        Param : mapObject -> L'objet MapObject dont on veut créer le modèle 3D
        Return : Une Promise qui retournera à terme le modèle 3D afin de pouvoir intéragir avec.
    */
    createMapObject3D(mapObject) {
        const modelPath = graphicObjects[mapObject.modelName];
        if (modelPath) {
            return this.createObject(mapObject.x, mapObject.y, mapObject.z, mapObject.ry, modelPath).then(sceneObject => {
                mapObject.sceneObject = sceneObject;
                return sceneObject;
            });
        }
    }


    createLaserMesh(color, startArray, endArray) {
        const start = new THREE.Vector3(...startArray);
        const end = new THREE.Vector3(...endArray);

        // Create a material
        const material = new THREE.MeshBasicMaterial({
          color: color
        });

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
    
    
    createCollisionBoxForGameObject(gameObject) {
        const objectBox = new THREE.Box3().setFromObject( gameObject.sceneObject );
        const size = new THREE.Vector3();
        objectBox.getSize(size);
        const height = size.y;

        let geometry;
        if (gameObject.collisionShape === "circle") {
            geometry = new THREE.CylinderGeometry( gameObject.collisionSize, gameObject.collisionSize, height, 8 );
        } else {
            geometry = new THREE.BoxGeometry(gameObject.collisionSize, height);
        }

        const material = new THREE.MeshBasicMaterial( {color: 0xffff00, transparent: true, opacity: 0.5} );
        const mesh = new THREE.Mesh( geometry, material );
        mesh.position.y = height / 2;
        mesh.rotation.y = gameObject.ry;
        return mesh;
    }

}

export default new Object3DFactory();
