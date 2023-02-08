from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from business.gameobjects.entity.bots.commands.IBotCommand import IBotCommand
from business.gameobjects.behaviour.IDestructible import IDestructible

from consumer.ConsumerManager import ConsumerManager
from consumer.webservices.messages.websocket.BotUpdateMessage import BotUpdateMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel


@dataclass(order=False)
class BotShootCommand(IBotCommand):
    action: str = field(default="shoot", compare=False)
    value: float = field(default=0.0, compare=False)

    def execute(self, arg: BotModel):
        """
        Contains the function to execute.
        """
        target = arg.shoot(self.value)
        ConsumerManager().websocket.send_message(BotUpdateMessage(bot_id=arg.id, target=target))

        # Hurting the target object
        if target.id:
            target_object = arg.bot_manager.game_manager.get_map_object_from_id(target.id)
            if target_object and isinstance(target_object, IDestructible):
                target_object.hurt(arg.equipment.weapon.damages)
