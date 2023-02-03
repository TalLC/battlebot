from consumer.webservices.messages.websocket.interfaces.IObjectMessage import IObjectMessage
from business.gameobjects.entity.bots.models.BotModel import BotModel


class BotCreateMessage(IObjectMessage):

    @property
    def bot(self) -> BotModel:
        return self._bot

    def __init__(self, bot: BotModel):
        super().__init__(msg_type="BotCreateMessage", object_id=bot.id)
        self._bot = bot

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        json = super().json()
        json |= {
            "x": self.bot.x,
            "z": self.bot.z,
            "ry": self.bot.ry,
            "team_color": self.bot.team.color,
            "shape_name": self.bot.shape_name.lower() if self.bot.shape_name else str(),
            "shape_size": self.bot.shape_size,
            "model_name": self.bot.model_name
        }
        return json
