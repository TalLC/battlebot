import logging
from math import fmod, pi

from business.gameobjects.tiles.Tile import Tile
from business.shapes.ShapesUtils import ShapesUtils
from consumer.ConsumerManager import ConsumerManager
from consumer.webservices.messages.websocket.BotMoveMessage import BotMoveMessage


class CollisionHandler:

    def __init__(self, bot):
        self._bot = bot
        self._collision_entity = None

    def check_env_collision(self, other):
        if isinstance(other, Tile):
            if other.tile_object.has_collision and other.tile_object.shape.intersection(self._bot.shape):
                return other.tile_object.name
            elif not other.is_walkable and (self._bot.shape.centroid.distance(other.shape.centroid) <
                                            ShapesUtils.get_radius(other.shape) + ShapesUtils.get_radius(
                        self._bot.shape)):
                return other.name

    def check_bot_collision(self, other):
        if isinstance(other, self._bot.__class__) and other != self._bot and other.shape.intersection(self._bot.shape):
            return other.name

    def check_collision(self):
        self._collision_entity = None
        neared_items = self._bot.bot_manager.game_manager.get_map_objects(
            bots=True, tiles=True, tile_objects=True, collision_only=True, radius=1, origin=self._bot.coordinates
        )

        for item in neared_items:
            self._collision_entity = self.check_env_collision(item) or self.check_bot_collision(item)
            if self._collision_entity is not None:
                return True

        return False

    def handle_collision(self):
        logging.debug(f'-------------{self._bot.name} collides with {self._collision_entity} -------------')
        self.knockback()
        self._bot.stun(1.5)

    def knockback(self, distance: float = 1.5, direction: float = None) -> None:
        """
        Quickly knock the bot back.
        """
        # TODO : Correction -> Côté back le bot recule à l'impact. Côté front, il bump lorsqu'il recommence à bouger.
        if not direction:
            direction = fmod(self._bot.ry - pi, 2 * pi)

        new_x, new_z = ShapesUtils.get_coordinates_at_distance(
            origin=(self._bot.x, self._bot.z), distance=distance, angle=direction)

        self._bot.set_position(new_x, new_z, self._bot.ry)

        ConsumerManager().websocket.send_message(BotMoveMessage(self._bot.id, self._bot.x, self._bot.z))
