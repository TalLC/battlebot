from pydantic import BaseModel


class BotActionRegisterModel(BaseModel):
    team_id: str
    bot_name: str
    bot_type: str = "warrior"
