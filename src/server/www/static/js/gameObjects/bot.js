import * as THREE from 'three';
import "../actionDefinition.js"
import {actions} from "../actions/actions.js"
import GameObject from './gameObject.js';


export default class Bot extends GameObject{
    constructor(construct){
        super(construct.id, "bot", construct.x, construct.z, construct.ry);

        this.teamColor = this.colorStrToNumber(construct.teamColor);
        this.shoot = false;
        this.hit = false;
        this.shieldHide = false;
        this.shieldRaise = false;
        this.avatarPath = construct.avatar;
        this.objBot = null;
        this.enrolled = false;
    }

    /*  
        Fonction : Permet la création/ajout à la scène du bot correspond à la classe.
        Param : viewController -> Classe permettant la gestion des interactions avec la scène.
        Return : N/A
    */
    create(viewController){
        viewController.createBot(this.x, this.ry, this.z, this.teamColor, 'avatar', 0).then(
            (objBot) => {
                // objBot.onPointerOver = this.onPointerOver.bind(this);
                // objBot.onconPointerOutlick = this.onPointerOut.bind(this);
                objBot.onclick = this.onClick.bind(this);

                this.objBot = objBot;
            }
        );
    }
    
    /* 
        Fonction : Permet l'appel à une action intéragissant avec le bot (action définit dans actionDefinition.js)
        Param : key -> contient le nom de l'action.
                param -> contient les paramètres nécéssaire à la réalisation de l'action.
        Return : N/A
    */
    action(key,param){
        actions[key].action.call(this, param);
    }


    colorStrToNumber(strColor) {
        // Default color
        let numberColor = new THREE.Color(0xffffff);
        
        try {
            // Parsing string color
            numberColor = numberColor = new THREE.Color(Number(strColor));
        } catch (error) {
            console.error(`Could not cast "${strColor}" into a number`);
        }

        return numberColor;
    }

    onPointerOver(e) {
        console.log("Over", this.id);
        this.material.color.set('hotpink');
        this.material.color.convertSRGBToLinear();
    }

    onPointerOut(e) {
        console.log("Out", this.id);
        this.material.color.set('orange');
        this.material.color.convertSRGBToLinear();
    }

    onClick(e) {
        console.log("Clicked!", this.id);
        objBot.traverse((o) => {
            if (o.isMesh) o.material = new THREE.MeshBasicMaterial(
                {
                    "color": 0x00ff00,
                    "transparent": false,
                    "opacity": 1.0
                }
            );;
        });
    }

}