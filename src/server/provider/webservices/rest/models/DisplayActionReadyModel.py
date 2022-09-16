from pydantic import BaseModel


class DisplayActionReadyModel(BaseModel):
    display_client_token: str
