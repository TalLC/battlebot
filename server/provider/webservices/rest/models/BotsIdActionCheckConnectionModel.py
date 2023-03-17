from pydantic import BaseModel


class BotsIdActionCheckConnectionModel(BaseModel):
    rest_id: str
    stomp_id: str
    mqtt_id: str
