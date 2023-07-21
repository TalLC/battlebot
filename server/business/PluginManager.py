import importlib
import logging
import sys

from business.interfaces import IPluginSpawn


class PluginManager:

    def my_plugin_spawn(self) -> IPluginSpawn:
        return self._my_plugin_spawn

    def plugins_spawn(self):
        return self._plugins_spawn

    # We are going to receive a list of plugins as parameter
    def __init__(self, map):
        self._plugins_spawn = None
        self._my_plugin_spawn = None
        self.load_config_plugins()
        self.plugin_spawn_selector(map)

    def load_config_plugins(self):
        from common.config import CONFIG_GAME

        self._plugins_spawn = CONFIG_GAME.plugins_spawn

    def plugin_spawn_selector(self, map):
        if self._plugins_spawn is None:
            self._plugins_spawn = []
        if self._plugins_spawn:
            for plugin_spawn in self._plugins_spawn:
                try :
                    logging.info('import du plugin ' + plugin_spawn)
                    self._my_plugin_spawn = importlib.import_module('plugins.spawn.' + plugin_spawn)
                    self._my_plugin_spawn = eval('self._my_plugin_spawn.' + plugin_spawn + '(map)')
                    logging.info('Le plugin ' + plugin_spawn + ' est importé !')
                    if not self._my_plugin_spawn.required():
                        logging.warning('Les conditions pour utiliser le plugin ' + plugin_spawn + ' ne sont pas remplies')
                        self._my_plugin_spawn = None
                    else:
                        break
                except :
                    logging.error('Le plugin ' + plugin_spawn + ' est introuvable !')
        if not self._my_plugin_spawn:
            try:
                logging.info('import du plugin RandomSpawn')
                self._my_plugin_spawn = importlib.import_module('plugins.spawn.' + 'RandomSpawn')
                self._my_plugin_spawn = eval('self._my_plugin_spawn.' + 'RandomSpawn' + '(map)')
                logging.info('Le plugin RandomSpawn est importé !')
            except :
                logging.error('Le plugin RandomSpawn qui est le plugin_spawn par default est introuvable ! Merci de le remettre pour le bon fonctionnement du jeu.')
                sys.exit()
