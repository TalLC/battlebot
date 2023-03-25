from pydantic import BaseModel


class BotsActionRegisterModel(BaseModel):
    team_id: str
    bot_name: str
    bot_type: str = "warrior"
