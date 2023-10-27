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
        const mapList = document.getElementById("choice-game-maplist");
        maps.forEach(element => {
            const button = document.createElement("button");
            button.type = "button";
            button.classList.add("list-group-item");
            button.classList.add("list-group-item-action");
            button.textContent = element.name;
            button.value = element.id;
            button.onclick = this.selectMap.bind(this, button, element);
            mapList.appendChild(button);
        });
    }

    deactivateAllButtons(){
        const mapList = document.getElementById("choice-game-maplist");
        Array.from(mapList.children).forEach(button => {
            button.classList.remove("active");
        })
        document.getElementById("choice-game-start-button").disabled = true;
    }

    selectMap(button, mapName){
        this.deactivateAllButtons();
        button.classList.add("active");
        console.log(mapName.id, mapName.name);
        sendRestMessage("GET", `/game/maps/${mapName.id}/info`).then((response) => response.json()).then((mapInfo) => {
            this.createPreviewInfoMap(mapInfo);
        })
        document.getElementById("choice-game-start-button").disabled = false;
    }

    createPreviewInfoMap(mapInfo){
        const mapPreview = document.getElementById("choice-game-map-preview");
        mapPreview.innerHTML = "";

        const preview = document.createElement("img");
        preview.classList.add("choice-game-img-preview");
        preview.src = `data:image/jpeg;base64,${mapInfo.preview}`;
        mapPreview.appendChild(preview);
        
        const name = document.createElement("h3");
        name.textContent = mapInfo.name;
        mapPreview.appendChild(name);


        const infos = document.createElement("ul");
        infos.classList.add("decorationless");
        const infoArray = [
            `Taille : ${mapInfo.height} * ${mapInfo.width}`,
            `Points d'apparition : ${mapInfo.spawners > 0 ? mapInfo.spawners : "aléatoire"}`,
            `Environnement : ${mapInfo.environment}`
        ]
        infoArray.forEach(info => {
            const li = document.createElement("li");
            li.innerText = info;
            infos.appendChild(li);
        })
        
        mapPreview.appendChild(infos);
    }
}

export default new MapSelector();
