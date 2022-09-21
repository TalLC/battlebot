from consumer.webservices.messages.websocket.models.MapUpdateMessage import MapUpdateMessage


class TileObjectDestroyedMessage(MapUpdateMessage):
    def __init__(self, x: int = None, z: int = None, destroyed: bool = False):
        super().__init__(x=x, z=z, destroyed=destroyed)
