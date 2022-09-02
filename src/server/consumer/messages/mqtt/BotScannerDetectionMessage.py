from consumer.messages.mqtt.interfaces.IScannerMessage import IScannerMessage


class BotScannerDetectionMessage(IScannerMessage):
    _MESSAGE_TYPE = "object_detection"

    def __init__(self, bot_id: str, objects_list: [dict]):
        data = objects_list
        super().__init__(bot_id, self._MESSAGE_TYPE, data)
