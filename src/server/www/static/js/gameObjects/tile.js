import "../actionDefinition.js"
import {actions} from "../actions/actions.js"

export default class Tile{
    constructor(construct){
        this.x = construct.x;
        this.z = construct.z;
        this.objTile = null;
        this.objObj = null;
    }

    /*  
        Fonction : Permet la création/ajout à la scène des tuile/objet correspond à la classe.
        Param : viewController -> Classe permettant la gestion des interactions avec la scène.
        Return : N/A
    */
    create(tile, obj, viewController){
        viewController.createObject(this.x, 0, this.z, tile).then((objTile) => {this.objTile = objTile});
        if (obj != 'air')
            viewController.createObject(this.x, 0.5, this.z, obj).then((objObj) => {this.objObj = objObj});
    }
    
    /* 
        Fonction : Permet l'appel à une action intéragissant avec les objets sur la map (action non définit pour l'instant)
        Param : key -> contient le nom de l'action.
                param -> contient les paramètres nécéssaire à la réalisation de l'action.
        Return : N/A
    */
    action(key,param){
        actions[key].action.call(this, param);
    }
}