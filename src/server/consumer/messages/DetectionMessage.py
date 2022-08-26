from consumer.messages.interfaces.IScannerMessage import IScannerMessage


class DetectionMessage(IScannerMessage):
    _INFO_TYPE = "object_detection"

    def __init__(self, bot_id: str, objects: list):
        super().__init__(bot_id, self._INFO_TYPE, objects)
