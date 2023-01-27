
export default class GameObject{
    constructor(id, type, x, y, z, ry) {
        this.id = id;
        this.type = type;
        this.x = x;
        this.y = y;
        this.z = z;
        this.ry = ry;
        this.debugBoxHelper;
    }

    render() {
        // Si on a une boxHelper, on l'update pour suivre le déplacement de l'objet
        if (this.debugBoxHelper) {
            this.debugBoxHelper.update();
        }
    }
}
