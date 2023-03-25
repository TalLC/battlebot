from pydantic import BaseModel


class DisplayClientsActionReadyModel(BaseModel):
    login_id: str
