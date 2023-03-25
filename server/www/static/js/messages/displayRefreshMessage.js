import logger from "../logger.js";
import BaseWsMessage from "./baseWsMessage.js";

export default class DisplayRefreshMessage extends BaseWsMessage {

    /**
     * Force le refresh de la page web. 
     */
    exec() {
        const delay = 5;

        logger.debug(`Refresh dans ${delay} secondes`);

        new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, delay * 1000);
        }).then(() => {
            window.location.reload();
        });
    }
}
