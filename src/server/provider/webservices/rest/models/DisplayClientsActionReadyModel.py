from pydantic import BaseModel


class DisplayActionReadyModel(BaseModel):
    client_token: str
