from pydantic import BaseModel


class DisplayClientsActionReadyModel(BaseModel):
    client_token: str
