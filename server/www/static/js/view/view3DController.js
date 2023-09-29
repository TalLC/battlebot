import * as THREE from "three";
import logger from "../logger.js";
import { OrbitControls } from "controls/OrbitControls";
import { FontLoader } from "loaders/FontLoader";
import { TextGeometry } from "geometries/TextGeometry";
import BotManager from "../botManager.js";
import Object3DFactory from "./object3DFactory.js";
import GameConfig from "../config.js";
import Debug from "../debug/debug.js";
import Bullet from "../gameObjects/bullet.js";

class CameraRenderer {
  constructor(origin, camera, renderer) {
    this.origin = origin;
    this.camera = camera;
    this.renderer = renderer;
  }
}

/**
 * Classe View3DController permettant de gérer l'affichage 3D du jeu.
 */
export default class View3DController {
  /**
   * Construit une instance de View3DController avec les dimensions spécifiées.
   * @param {Object} gameManager - Gestionnaire de jeu.
   * @param {string} viewContainerId - ID du conteneur HTML pour l'affichage 3D.
   * @param {number} width - Largeur de la vue 3D.
   * @param {number} height - Hauteur de la vue 3D.
   */
  constructor(gameManager, viewContainerId) {
    this.gameManager = gameManager;
    this.container = document.getElementById(viewContainerId);
    this.threejsCanvas = this.container.querySelector("#threejs-canvas");
    this.previewButton = document.getElementById("button-preview-toggle");
    this.previewButton.onclick = this.togglePreview.bind(this, this.previewButton);
    this.cameraContainer = document.getElementById('cameras-container');

    this.renderers = [];
    this.renderer = new THREE.WebGLRenderer({ canvas: this.threejsCanvas });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    
    // Création de la scene principale
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0xa0d0da);
    this.scene.fog = new THREE.Fog(0xa0d0da, 0.5, 500);

    this.initLight(this.scene);

    // Prise en charge du redimensionnement de fenêtre
    window.onresize = this.resize.bind(this);

    if (GameConfig().isDebug) {
      this.debug = new Debug(this, "debug-container");
      this.container.onpointermove = this.debug.updateRaycastedObjects.bind(this.debug);
      this.container.ondblclick = this.debug.clickObject.bind(this.debug);
    }
  }

  togglePreview(button) {
    const isHidden = this.cameraContainer.hidden;
    if (isHidden) {
      button.innerHTML = '<i class="bi bi-chevron-double-right"></i>';
      this.cameraContainer.hidden = false;
    } else {
      button.innerHTML = '<i class="bi bi-chevron-double-left"></i>';
      this.cameraContainer.hidden = true;
    }
  }

  /**
   * Fonction pour le rendu de la scène.
   */
  render() {
    if (GameConfig().isDebug) this.debug.render();
    this.renderers.forEach(cr => {
      cr.renderer.render(this.scene, cr.camera);
    })
  }

  createCameraPreviews() {
    // Ajout de la preview principale
    this.registerMainPreviewCamera();

    // Ajout des previews pour chaque Bot
    Object.values(BotManager.bots).forEach(bot => {
      this.registerBotPreviewCamera(bot);
    });
  }

  /**
   * Fonction pour définir la caméra utilisée pour le rendu.
   */
  setCurrentCamera(camera) {
    this.renderers
      .find(elem => elem.origin === 'main')
      .camera = camera;
  }

  getCurrentCamera() {
    return this.renderers
      .find(elem => elem.origin === 'main').camera;
  }

  /**
   * Fonction pour ajuster la taille de la scène lors du redimensionnement de la fenêtre.
   */
  resize() {
    this.globalCamera.aspect = window.innerWidth / window.innerHeight;
    this.globalCamera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.render();
  }

  /**
   * Fonction pour démarrer l'affichage de la scène et des éléments de debug si besoin.
   */
  start() {
    // Création de la caméra
    this.globalCamera = this.createCamera({ x: 64, y: 64, z: 64 }, { x: 16, y: 0, z: 16 });

    // Caméra courante
    this.renderers.push(new CameraRenderer('main', this.globalCamera, this.renderer));

    // Création des previews clickable de caméras
    this.createCameraPreviews();
    
    // Affichage du viewport Three.js
    this.container.hidden = false;

    if (GameConfig().isDebug) this.debug.start();
  }

  /**
   * Fonction pour afficher un message de "hit" sur un objet donné.
   * @param {Object} obj - L'objet pour lequel afficher le message de hit.
   */
  showHurtMessageForObject(obj) {
    let font;

    new Promise((resolve) => {
      // Load the font
      let loader = new FontLoader();
      loader.load("static/fonts/helvetiker_bold.typeface.json", function (loadedFont) {
        font = loadedFont;
        resolve();
      });
    })
      .then(() => {
        // Create the text using TextGeometry
        const textGeometry = new TextGeometry("<hit>", {
          font: font,
          size: 0.5,
          height: 0.001
        });
        const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00, transparent: true });
        const textMesh = new THREE.Mesh(textGeometry, textMaterial);

        // Position the text in the scene
        textMesh.position.set(obj.x, obj.y + 5.0, obj.z);
        textMesh.lookAt(this.globalCamera.position);

        // Add the text to the scene
        this.scene.add(textMesh);
        return textMesh;
      })
      .then((textMesh) => {
        // Diminuer l'opacité pour rendre le texte invisible
        return new Promise((resolve) => {
          let opacity = 1;
          const interval = setInterval(() => {
            opacity -= 0.1;
            textMesh.material.opacity = opacity;
            textMesh.lookAt(this.globalCamera.position);
            if (opacity <= 0) {
              clearInterval(interval);
              resolve(textMesh);
            }
          }, 100);
        });
      })
      .then((textMesh) => {
        // Supprimer l'objet de la scene
        this.disposeSceneObject(textMesh);
      });
  }

  /**
   * Fonction pour afficher le tir d'un bot.
   * @param {Object} bot - Le bot qui tire.
   * @param {Object} target - Les coordonnées de la cible.
   */
  shootTo(bot, target) {
    const bulletY = 1.8;
    const vTarget = new THREE.Vector3(target.x, bulletY, target.z);
    const bullet = new Bullet(bot.x, bulletY, bot.z, 0.0, bot.teamColor);
    Object3DFactory.createBullet3D(bullet).then((bulletSceneObject) => {
      bulletSceneObject.lookAt(vTarget);
      bulletSceneObject.rotation.y += Math.PI / 2;
      this.scene.add(bulletSceneObject);
      bullet.moveTo(target);
    });
  }

  /**
   * Fonction pour initialiser l'éclairage de la scène.
   */
  initLight(scene) {
    logger.debug("initialisation light");
    //Création de la lumière ambiante
    const light = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(light);

    //Création de la lumière orientée
    const directionalLight = new THREE.DirectionalLight(0xe6faff, 1.0);
    directionalLight.position.x = 8.0;
    directionalLight.position.y = 16.0;
    directionalLight.position.z = 8.0;
    directionalLight.target.position.set(16, 0, 16);
    directionalLight.target.updateMatrixWorld();
    directionalLight.castShadow = true;
    directionalLight.shadow.camera.top = 32;
    directionalLight.shadow.camera.bottom = -32;
    directionalLight.shadow.camera.left = 32;
    directionalLight.shadow.camera.right = -32;
    directionalLight.shadow.bias = -0.01;

    directionalLight.shadow.mapSize.width = 1024; // default
    directionalLight.shadow.mapSize.height = 1024; // default
    directionalLight.shadow.camera.near = 0.001; // default
    directionalLight.shadow.camera.far = 55;
    directionalLight.shadow.radius = 1;
    scene.add(directionalLight);
  }

  /**
   * Fonction pour créer une caméra afin de visualiser la scène.
   * @param {Object} position - Position de la caméra en x, y et z.
   * @param {Object} lookAt - Position vers laquelle regarde la caméra en x, y et z.
   * @returns {THREE.PerspectiveCamera} La caméra créée.
   */
  createCamera(position, lookAt) {
    const camera = new THREE.PerspectiveCamera(18, window.innerWidth / window.innerHeight, 1, 500);
    camera.position.set(position.x, position.y, position.z);
    this.controls = new OrbitControls(camera, this.renderer.domElement);
    this.controls.target.set(lookAt.x, lookAt.y, lookAt.z);
    this.controls.update();

    return camera;
  }

  registerMainPreviewCamera() {    
    const cameraPreview = this.registerPreviewCamera("Vue globale", "main-preview", this.globalCamera);
    cameraPreview.onclick = this.setCameraToDefault.bind(this);
  }

  registerBotPreviewCamera(bot) {    
    const cameraPreview = this.registerPreviewCamera(bot.name, bot.id, bot.camera, '#' + bot.teamColor.getHexString());
    cameraPreview.onclick = this.setCameraFromPreview.bind(this, bot);
  }

  registerPreviewCamera(name, id, camera, borderColor) {
    const [cameraPreview, cameraPreviewCanvas] = this.createHtmlCameraPreview(name, borderColor);

    const renderer = new THREE.WebGLRenderer({ canvas: cameraPreviewCanvas });
    renderer.setSize(cameraPreview.offsetWidth, cameraPreview.offsetHeight);
    renderer.shadowMap.enabled = true;

    this.renderers.push(new CameraRenderer(id, camera, renderer));

    return cameraPreview;
  }
  
  createHtmlCameraPreview(name, borderColor) {
    const cameraPreview = document.createElement('div');
    
    const cameraPreviewName = document.createElement('h3');
    cameraPreviewName.innerText = name;

    cameraPreview.classList.add('camera-preview');
    cameraPreview.classList.add('row');
    cameraPreview.classList.add('g-0');
    if (borderColor) {
      cameraPreview.style.borderColor = borderColor;
    }

    const cameraPreviewCanvas = document.createElement('canvas');
    cameraPreviewCanvas.classList.add('canvas-preview');
    cameraPreview.appendChild(cameraPreviewCanvas);

    this.cameraContainer.appendChild(cameraPreviewName);
    this.cameraContainer.appendChild(cameraPreview);

    return [cameraPreview, cameraPreviewCanvas];
  }

  setCameraToDefault() {
    this.setCurrentCamera(this.globalCamera);

    if (GameConfig().isDebug) {
      this.debug.deselectObject();
    }
  }

  setCameraFromPreview(bot) {
    this.setCurrentCamera(bot.camera);

    if (GameConfig().isDebug) {
      this.debug.setSelectedObject(bot.sceneObject.children[0], bot);
      this.debug.writeBotInformations(bot);
      this.debug.debugUi.setRemoteHidden(false);
    }
  }

  /**
   * Fonction pour effacer complètement un objet de la scène ThreeJs.
   * @param {THREE.Object3D} sceneObject - L'objet à supprimer.
   */
  disposeSceneObject(sceneObject) {
    if (!(sceneObject instanceof THREE.Object3D)) return false;

    if (sceneObject.geometry) sceneObject.geometry.dispose();

    if (sceneObject.material) {
      if (sceneObject.material instanceof Array) {
        sceneObject.material.forEach((material) => material.dispose());
      } else {
        sceneObject.material.dispose();
      }
    }
    sceneObject.removeFromParent();
  }
}
