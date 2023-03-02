import sys
import json
from pathlib import Path

# Ce script passe juste le mode debug de la config serveur à vrais ou faux

GAME_CONFIG_PATH = Path('conf', 'game.json')
GAME_CONFIG = json.loads(GAME_CONFIG_PATH.read_text(encoding='utf-8'))

if len(sys.argv) > 1:
    if sys.argv[1] == "debug=true":
        GAME_CONFIG['is_debug'] = True
    else:
        GAME_CONFIG['is_debug'] = False
    GAME_CONFIG_PATH.write_text(json.dumps(GAME_CONFIG))
