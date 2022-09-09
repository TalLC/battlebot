from business.gameobjects.entity.bots.scanner.DetectedObject import DetectedObject
from consumer.brokers.messages.mqtt.interfaces.IScannerMessage import IScannerMessage


class BotScannerDetectionMessage(IScannerMessage):
    _MESSAGE_TYPE = "object_detection"

    def __init__(self, bot_id: str, detected_object_list: [DetectedObject]):
        data = list()
        for detected in detected_object_list:
            x = {
                "name": detected.name,
                "angle": detected.angle
             }
            data.append(x)
        super().__init__(bot_id, self._MESSAGE_TYPE, data)
