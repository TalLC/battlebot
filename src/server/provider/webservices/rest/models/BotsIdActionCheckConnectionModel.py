from pydantic import BaseModel


class BotsIdActionCheckConnectionModel(BaseModel):
    request_id: str
    stomp_id: str
    mqtt_id: str
