from math import pi

from business.gameobjects.entity.bots.equipments.scanner.DetectedObject import DetectedObject
from consumer.brokers.messages.mqtt.interfaces.IScannerMessage import IScannerMessage


class BotScannerDetectionMessage(IScannerMessage):

    def __init__(self, bot_id: str, detected_object_list: [DetectedObject]):
        data = list()
        for detected in detected_object_list:

            data.append(
                {
                    "from": detected.a_from,
                    "to": detected.a_to,
                    "name": detected.name,
                    "distance": detected.distance
                }
            )
        super().__init__(bot_id=bot_id, msg_type="object_detection", data=data)
