from consumer.webservices.messages.websocket.interface.IMapUpdateMessage import IMapUpdateMessage


class TileCreateMessage(IMapUpdateMessage):
    def __init__(self, x: int = None, z: int = None, create_tile: str = "", create_object: str = ""):
        super().__init__(x=x, z=z, create_tile=create_tile, create_object=create_object)
