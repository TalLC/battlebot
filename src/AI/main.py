import sys
import json
import logging
from time import sleep
from threading import Event, Thread
from lib_ai.BotAi import BotAi


from pathlib import Path

G_BOT_ID_TMP_FILE = Path('bot_id.tmp')
G_BOT_CONFIG = json.loads(Path('bot1.json').read_text())


def check_for_existing_bot_id() -> str:
    """
    If a bot was previously registered, we read the bot_id.
    """
    if G_BOT_ID_TMP_FILE.exists():
        return G_BOT_ID_TMP_FILE.read_text()
    else:
        return ""


def read_scanner_queue(e: Event, bot: BotAi):
    while not e.is_set():
        scanner_message = bot.read_scanner()
        logging.info(f"[SCANNER] {scanner_message}")


def read_game_queue(e: Event, bot: BotAi):
    while not e.is_set():
        game_message = bot.read_game_message()
        logging.info(f"[GAME] {game_message}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # Creating a new Bot
    with BotAi(G_BOT_CONFIG['bot_name'], G_BOT_CONFIG['team_id']) as bot1:

        # Bot enrollment
        try:
            # If we crashed after enrolling the bot, we re-use the same bot_id if it was stored
            bot_id = bot1.enroll(check_for_existing_bot_id())
        except BotAi.RestException as ex:
            # If the bot id is invalid
            if ex.name == 'BOT_DOES_NOT_EXISTS':
                # Bot id was invalid, deleting tmp file
                G_BOT_ID_TMP_FILE.unlink(missing_ok=True)
                # Enrolling as new bot
                bot_id = bot1.enroll()
            else:
                logging.exception(str(ex))
                sys.exit()

        # Writing new bot id to tmp file
        G_BOT_ID_TMP_FILE.write_text(bot_id)

        # Bot scanner messages handler thread
        scanner_message_thread_event = Event()
        scanner_message_thread = Thread(target=read_scanner_queue, args=(scanner_message_thread_event, bot1)).start()

        # Game messages handler thread
        game_message_thread_event = Event()
        game_message_thread = Thread(target=read_game_queue, args=(game_message_thread_event, bot1)).start()

        try:
            while True:
                # Analyze stuff
                # Make complex decisions
                # Go to sleep
                sleep(0.1)
        except KeyboardInterrupt:
            # Closing messages reading threads
            scanner_message_thread_event.set()
            game_message_thread_event.set()

            # Closing bot connections
            bot1.close()

            # Removing temp file
            G_BOT_ID_TMP_FILE.unlink(missing_ok=True)
