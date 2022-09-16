from consumer.webservices.messages.interfaces.IMapUpdateMessage import IMapUpdateMessage


class TileObjectDestroyedMessage(IMapUpdateMessage):
    def __init__(self, x: int = None, z: int = None, destroyed: bool = False):
        super().__init__(x=x, z=z, destroyed=destroyed)
