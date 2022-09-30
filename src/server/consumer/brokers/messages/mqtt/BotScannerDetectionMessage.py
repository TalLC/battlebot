from business.gameobjects.entity.bots.scanner.DetectedObject import DetectedObject
from consumer.brokers.messages.mqtt.interfaces.IScannerMessage import IScannerMessage


class BotScannerDetectionMessage(IScannerMessage):

    def __init__(self, bot_id: str, detected_object_list: [DetectedObject]):
        data = list()
        for detected in detected_object_list:
            data.append(
                {
                    "name": detected.name,
                    "angle": detected.angle
                }
            )
        super().__init__(bot_id=bot_id, msg_type="object_detection", data=data)
