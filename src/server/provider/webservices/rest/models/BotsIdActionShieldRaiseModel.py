from pydantic import BaseModel


class BotIdActionShieldRaiseModel(BaseModel):
    action: str
