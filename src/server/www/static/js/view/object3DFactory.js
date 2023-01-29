import * as THREE from 'three';


class Object3DFactory {
    constructor() {}


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

    getPointInBetweenByPerc(pointA, pointB, percentage) {
        var dir = pointB.clone().sub(pointA);
        var len = dir.length();
        dir = dir.normalize().multiplyScalar(len*percentage);
        return pointA.clone().add(dir);
    }
}

export default new Object3DFactory();
