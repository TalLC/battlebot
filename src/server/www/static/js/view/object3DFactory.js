import * as THREE from 'three';


class Object3DFactory {
    constructor() {}


    createLaserMesh(color, startArray, endArray) {
        const start = new THREE.Vector3(...startArray);
        const end = new THREE.Vector3(...endArray);

        // Create a material
        let lineMaterial = new THREE.MeshBasicMaterial({
          color: color
        });
      
        //calculate the distance between start and end point
        let distance = start.distanceTo(end);
        
        //calculate the number of segments needed
        const desired_detail_level = 2;
        let segments = Math.ceil(distance / desired_detail_level);
        
        // Create a path for the tube
        let path = new THREE.CatmullRomCurve3([start, end]);
        
        // Create the tube geometry
        let tubeGeometry = new THREE.TubeGeometry(
          path,
          segments,
          0.15,
          8,
          true
        );
      
        // Create the tube mesh
        return new THREE.Mesh(tubeGeometry, lineMaterial);
    }
    
    
    createCollisionBoxForGameObject(gameObject) {
        const objectBox = new THREE.Box3().setFromObject( gameObject.sceneObject );
        const size = new THREE.Vector3();
        objectBox.getSize(size);
        const height = size.y;

        let geometry;
        console.log('gameObject.collisionShape', gameObject.collisionShape);
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
