import logger from "./logger.js";
import sendRestMessage from "./utils/rest.js";

/**
 * Singleton gérant la selection de map.
 */

let instance;

export class MapSelector {
    constructor() {
        if (!instance) {
            instance = this;
        }

        return instance;
    }
 
    /**
     * Crée la liste des boutons en fonction des maps disponible pour l'html
     */
    createChoiceGameMapButtons(maps){
        const maplist = document.getElementById("choice-game-maplist");
        maps.forEach(element => {
            const button = document.createElement("button");
            button.type = "button";
            button.classList.add("list-group-item");
            button.classList.add("list-group-item-action");
            button.textContent = element.name;
            button.value = element.id;
            button.onclick = this.selectMap.bind(this, button, element);
            maplist.appendChild(button);
        });
    }

    desactiveAllButtons(){
        const maplist = document.getElementById("choice-game-maplist");
        Array.from(maplist.children).forEach(button => {
            button.classList.remove("active");
        })
    }

    selectMap(button, mapName){
        this.desactiveAllButtons();
        button.classList.add("active");
        console.log(mapName.id, mapName.name);
        sendRestMessage("GET", `/game/maps/${mapName.id}/info`).then((response) => response.json()).then((mapInfo) => {
            this.createPreviewInfoMap(mapInfo);
        })
    }

    createPreviewInfoMap(mapInfo){
        const mapPreview = document.getElementById("choice-game-map-preview");
        mapPreview.innerHTML = "";

        const preview = document.createElement("img");
        preview.classList.add("choice-game-preview");
        preview.src = `data:image/jpeg;base64,${mapInfo.preview}`;
        mapPreview.appendChild(preview);
        
        const name = document.createElement("h4");
        name.textContent = mapInfo.name;
        mapPreview.appendChild(name);


        const info = document.createElement("p");
        const infoArray = [
            `Taille MAP : ${mapInfo.height} * ${mapInfo.width}`,
            `Nombre de Spawn : ${mapInfo.spawners}`,
            `Environnement : ${mapInfo.environment}`
        ]
        const tmp = infoArray.join('\ni');
        console.log(tmp);
        info.textContent = tmp;
        mapPreview.appendChild(info);
    }
}

export default new MapSelector();
