from math import pi

from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from consumer.brokers.messages.mqtt.interfaces.IScannerMessage import IScannerMessage


class BotScannerDetectionMessage(IScannerMessage):

    def __init__(self, bot_id: str, detected_objects: [DetectedObject]):
        super().__init__(
            bot_id=bot_id,
            msg_type="object_detection",
            data=list([o.json() for o in detected_objects])
        )
