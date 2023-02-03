from consumer.webservices.messages.websocket.interfaces.IBotMessage import IBotMessage
from business.gameobjects.entity.bots.models.BotModel import BotModel


class BotCreateMessage(IBotMessage):

    @property
    def bot(self) -> BotModel:
        return self._bot

    def __init__(self, bot: BotModel):
        super().__init__(msg_type="BotCreateMessage", bot_id=bot.id)
        self._bot = bot

    def __add__(self, other):
        raise NotImplementedError()

    def json(self) -> dict:
        return {
            'id': self.bot.id,
            'msg_type': self.msg_type,
            "x": self.bot.x,
            "z": self.bot.z,
            "ry": self.bot.ry,
            "team_color": self.bot.team.color,
            "shape_name": self.bot.shape_name.lower() if self.bot.shape_name else str(),
            "shape_size": self.bot.shape_size,
            "model_name": self.bot.model_name
        }
