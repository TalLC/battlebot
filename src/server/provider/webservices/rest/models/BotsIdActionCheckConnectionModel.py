from pydantic import BaseModel


class BotIdActionCheckConnectionModel(BaseModel):
    request_id: str
    stomp_id: str
    mqtt_id: str
