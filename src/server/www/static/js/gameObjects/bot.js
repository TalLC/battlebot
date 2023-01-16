import "../actionDefinition.js"
import {actions} from "../actions/actions.js"

export default class Bot{
    constructor(construct){
        this.id = construct.id;
        this.x = construct.x;
        this.z = construct.z;
        this.ry = construct.ry;
        this.teamColor = construct.teamColor;
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
                this.objBot = objBot
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
}