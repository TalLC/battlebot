from pydantic import BaseModel


class BotIdActionTurnModel(BaseModel):
    direction: str
