from typing import List

from consumer.webservices.messages.websocket.interfaces.IObjectMessage import IObjectMessage
from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject


class DebugBotDetectedObjects(IObjectMessage):

    def __init__(self, object_id: str, detected_objects: List[DetectedObject], interval: float):
        super().__init__(msg_type="DebugBotDetectedObjects", object_id=object_id)
        self._detected_objects = detected_objects
        self._interval = interval

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        json |= {
            'interval': self._interval,
            'objects': [
                {
                    'object_type': o.object_type,
                    'x': o.x,
                    'z': o.z
                } for o in self._detected_objects]
        }
        return json
