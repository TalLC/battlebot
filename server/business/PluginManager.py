from __future__ import annotations
import importlib
import logging
import sys
from typing import TYPE_CHECKING, List
from common.Singleton import SingletonABCMeta

from business.interfaces.IPluginManager import IPluginManager

if TYPE_CHECKING:
    from business.maps.Map import Map
    from business.interfaces.IPluginSpawn import IPluginSpawn


class PluginManager(IPluginManager, metaclass=SingletonABCMeta):

    DEFAULT_SPAWN_PLUGIN_NAME = "RandomSpawn"

    @classmethod
    def get_plugin_spawn_for_map(cls, game_map: Map) -> IPluginSpawn:
        logging.debug(f"Recherche du plugin disponible pour la map {game_map.id}")
        spawn_plugins = PluginManager.__get_available_spawn_plugins()
        selected_plugin = None

        # On parcourt les plugins pour trouver le premier compatible
        if len(spawn_plugins):
            for plugin_spawn_name in spawn_plugins:
                try:
                    logging.info(f'Import du plugin {plugin_spawn_name}')
                    selected_plugin = importlib.import_module('plugins.spawn.' + plugin_spawn_name)
                    selected_plugin = eval('selected_plugin.' + plugin_spawn_name + '(game_map)')
                    if not selected_plugin.required():
                        logging.warning(f'Les conditions pour utiliser le plugin "{plugin_spawn_name}" ne sont '
                                        f'pas remplies')
                        selected_plugin = None
                        break
                    else:
                        logging.info(f'Le plugin "{plugin_spawn_name}" est importé !')
                        break
                except:
                    logging.error(f'Le plugin "{plugin_spawn_name}" est introuvable !')

        # Aucun plugin ne correspondait, on prend le plugin random par défaut
        if selected_plugin is None:
            try:
                logging.info(f'Import du plugin {cls.DEFAULT_SPAWN_PLUGIN_NAME}')
                selected_plugin = importlib.import_module(f'plugins.spawn.{cls.DEFAULT_SPAWN_PLUGIN_NAME}')
                selected_plugin = eval(f'selected_plugin.{cls.DEFAULT_SPAWN_PLUGIN_NAME}(game_map)')
                logging.info(f'Le plugin {cls.DEFAULT_SPAWN_PLUGIN_NAME} est importé !')
            except:
                logging.error(f'Le plugin de spawn par défaut {cls.DEFAULT_SPAWN_PLUGIN_NAME} est introuvable ! '
                              f'Merci de le remettre pour le bon fonctionnement du jeu.')
                sys.exit()
        return selected_plugin

    @staticmethod
    def __get_available_spawn_plugins() -> List[str]:
        from common.config import CONFIG_GAME
        plugins_spawn_config = CONFIG_GAME.plugins_spawn
        return plugins_spawn_config if plugins_spawn_config is not None else list()
