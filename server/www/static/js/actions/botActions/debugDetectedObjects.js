import { ActionDefinition, actions } from "../actions.js";
import * as THREE from "three";
import BotManager from "../../botManager.js";
import GameManager from "../../gameManager.js";

function eventWrapper(message) {
    return message;
}

function actionSelector(message) {
    return message.msg_type === "DebugBotDetectedObjects";
}

function action(message) {
    let scene = GameManager().viewController.scene;
    let bot = BotManager.getBotObjectFromId(message.id);

    createTemporaryModelsFromObjects(scene, message.objects, bot.teamColor, message.interval * 1000);
}

function createTemporaryModel(scene, object, materialColor, interval) {
    let geometry, material, mesh, destroyTimeout;

    switch (object.object_type) {
        case "tree":
            geometry = new THREE.CylinderGeometry(0.5, 0.5, 2.0, 16);
            break;
        case "rock":
            geometry = new THREE.CylinderGeometry(0.5, 0.5, 0.5, 16);
            break;
        case "tile":
            geometry = new THREE.BoxGeometry(1.0, 1.0, 1.0);
            break;
        case "bot":
            geometry = new THREE.SphereGeometry(0.5, 16, 16);
            break;
        default:
            console.error(`Unknown object type: ${object.object_type}`);
            return;
    }

    material = new THREE.MeshStandardMaterial({
        color: materialColor
    });
    mesh = new THREE.Mesh(geometry, material);

    mesh.position.x = object.x;
    mesh.position.z = object.z;
    switch (object.object_type) {
        case "tree":
            mesh.position.y = 1.0;
            break;
        case "rock":
            mesh.position.y = 1.0;
            break;
        case "bot":
            mesh.position.y = 3.0;
            break;
        default:
            break;
    }

    scene.add(mesh);

    const promise = new Promise((resolve, reject) => {
        destroyTimeout = setTimeout(() => {
            scene.remove(mesh);
            resolve();
        }, interval);
    });

    promise.catch(() => {
        scene.remove(mesh);
        clearTimeout(destroyTimeout);
    });

    return promise;
}

function createTemporaryModelsFromObjects(scene, objects, materialColor, interval) {
    const promises = [];

    for (let object of objects) {
        promises.push(createTemporaryModel(scene, object, materialColor, interval));
    }

    return Promise.all(promises);
}

actions.debugDetectedObjects = new ActionDefinition(eventWrapper, actionSelector, action);
