from pydantic import BaseModel


class BotsIdActionTurnModel(BaseModel):
    direction: str
