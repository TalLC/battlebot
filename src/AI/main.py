import sys
import json
import logging
import random
from datetime import datetime, timedelta
from time import sleep
from threading import Event, Thread
from battlebotslib.BotAi import BotAi
from queue import SimpleQueue

from pathlib import Path

G_BOT_ID_TMP_FILE = Path('bot_id.tmp')
G_BOT_CONFIG = json.loads(Path('bot1.json').read_text())
G_GAME_IS_STARTED = False

G_BOT_HEALTH = 100
G_BOT_IS_MOVING = False
G_BOT_IS_TURNING = False
G_BOT_TURN_DIRECTION = str()

G_BOT_TARGETS_QUEUE = SimpleQueue()


def check_for_existing_bot_id() -> str:
    """
    If a bot was previously registered, we read the bot_id.
    """
    if G_BOT_ID_TMP_FILE.exists():
        return G_BOT_ID_TMP_FILE.read_text()
    else:
        return ""


def thread_read_scanner_queue(e: Event, bot_ai: BotAi):
    """
    Thread continuously reading messages from the bot scanner queue.
    """
    while not e.is_set():
        scanner_message = bot_ai.read_scanner()
        logging.debug(f"[SCANNER] {scanner_message}")
        handle_scanner_message(scanner_message)


def thread_read_game_queue(e: Event, bot_ai: BotAi):
    """
    Thread continuously reading messages from the game queue.
    """
    while not e.is_set():
        game_message = bot_ai.read_game_message()
        logging.debug(f"[GAME] {game_message}")
        handle_game_message(game_message)


def handle_scanner_message(message: dict):
    """
    Handle a new scanner message.
    """
    try:
        if 'msg_type' in message and message['msg_type'] == 'object_detection':
            for detected_object in message['data']:
                # Checking if an object is detected
                if detected_object['name'] is not None:
                    angle = (detected_object['from'] + detected_object['to']) / 2
                    logging.info(
                        f"[SCANNER] {detected_object['name']} detected at a distance of "
                        f"{detected_object['distance']} ({angle}°)"
                    )

                    # We want to shoot at trees and bots
                    if detected_object['object_type'] in ['tree', 'bot']:
                        G_BOT_TARGETS_QUEUE.put(angle)
        else:
            logging.error("Not an object detection scanner message")
    except:
        logging.error(f"Bad scanner message format:\n{message}")


def handle_game_message(message: dict):
    """
    Handle a new game message.
    """
    try:
        if 'msg_type' in message:
            # Health update message
            if message['msg_type'] == 'health_status':
                global G_BOT_HEALTH
                current_health = message['data']['value']
                G_BOT_HEALTH = current_health
                logging.info(f"[BOT] Health: {current_health}")
            # Game update message
            if message['msg_type'] == 'game_status':
                global G_GAME_IS_STARTED
                G_GAME_IS_STARTED = message['data']
            # Bot moving update message
            elif message['msg_type'] == 'moving_status':
                global G_BOT_IS_MOVING
                # The message tells us the bot has stopped moving
                if not message['data']['value']:
                    # Bot has been stopped
                    G_BOT_IS_MOVING = False
            # Bot turning update message
            elif message['msg_type'] == 'turning_status':
                global G_BOT_IS_TURNING
                # The message tells us the bot has stopped turning
                if not message['data']['value']:
                    # Bot has been stopped
                    G_BOT_IS_TURNING = False
        else:
            logging.error("Not a game message")
    except:
        logging.error(f"Bad game message format:\n{message}")


def get_opposite_direction(direction: str) -> str:
    if direction.lower() == 'left':
        return 'right'
    elif direction.lower() == 'right':
        return 'left'
    else:
        return 'stop'


def show_bot_stats():
    logging.info(f"Health: {G_BOT_HEALTH}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # Creating a new Bot
    with BotAi(G_BOT_CONFIG['bot_name'], G_BOT_CONFIG['team_id']) as bot:
        def stop():
            # Closing messages reading threads
            scanner_message_thread_event.set()
            game_message_thread_event.set()

            # Removing temp file
            G_BOT_ID_TMP_FILE.unlink(missing_ok=True)

        # Bot enrollment
        try:
            # If we crashed after enrolling the bot, we re-use the same bot_id if it was stored
            bot_id = bot.enroll(check_for_existing_bot_id())
        except BotAi.RestException as ex:
            # If the bot id is invalid
            if ex.name == 'BOT_DOES_NOT_EXISTS':
                # Bot id was invalid, deleting tmp file
                G_BOT_ID_TMP_FILE.unlink(missing_ok=True)
                # Enrolling as new bot
                bot_id = bot.enroll()
            else:
                logging.exception(str(ex))
                sys.exit()

        # Writing new bot id to tmp file
        G_BOT_ID_TMP_FILE.write_text(bot_id)

        # Bot scanner messages handler thread
        scanner_message_thread_event = Event()
        Thread(target=thread_read_scanner_queue, args=(scanner_message_thread_event, bot)).start()

        # Game messages handler thread
        game_message_thread_event = Event()
        Thread(target=thread_read_game_queue, args=(game_message_thread_event, bot)).start()

        try:
            # Randomize directions and durations
            seed = random.randrange(sys.maxsize)
            rand_gen = random.Random(seed)

            # Waiting for the game to start
            while not G_GAME_IS_STARTED:
                sleep(0.1)

            # Game is started
            show_bot_stats()

            try:
                # Big AI time
                bot.move('start')
                G_BOT_IS_MOVING = True

                sleep(rand_gen.randint(2, 7))

                G_BOT_TURN_DIRECTION = 'right'
                bot.turn(G_BOT_TURN_DIRECTION)
                G_BOT_IS_TURNING = True

                last_direction_change_ts = datetime.now()
                while G_BOT_HEALTH > 0 and G_GAME_IS_STARTED:
                    # Analyze stuff
                    # Compiling matrix
                    # Optimizing core mainframe
                    # Make vary much complex decisions
                    # Go to sleep

                    if not G_BOT_TARGETS_QUEUE.empty():
                        angle = G_BOT_TARGETS_QUEUE.get(block=False)
                        bot.shoot(angle)

                    if G_BOT_IS_MOVING:
                        # If the bot is urning en rond for at least x seconds, we stop turning
                        if G_BOT_IS_TURNING and datetime.now() - last_direction_change_ts \
                                > timedelta(seconds=rand_gen.randint(1, 4)):
                            last_direction_change_ts = datetime.now()
                            bot.turn('stop')
                            G_BOT_IS_TURNING = False
                        # If the bot is going forward for at least x seconds, we make him turn
                        elif not G_BOT_IS_TURNING and datetime.now() - last_direction_change_ts \
                                > timedelta(seconds=rand_gen.randint(2, 7)):
                            last_direction_change_ts = datetime.now()
                            G_BOT_TURN_DIRECTION = rand_gen.choice(['left', 'right'])
                            bot.turn(G_BOT_TURN_DIRECTION)
                            G_BOT_IS_TURNING = True
                    else:
                        # G_BOT_TURN_DIRECTION = get_opposite_direction(G_BOT_TURN_DIRECTION)
                        G_BOT_TURN_DIRECTION = rand_gen.choice(['left', 'right'])
                        bot.turn(G_BOT_TURN_DIRECTION)
                        G_BOT_IS_TURNING = True
                        sleep(rand_gen.randint(1, 10))
                        bot.move('start')
                        G_BOT_IS_MOVING = True

                    sleep(0.1)

            except BotAi.RestException as ex:
                if ex.name == 'BOT_IS_STUNNED':
                    pass

            if not G_GAME_IS_STARTED:
                logging.info("Game has been stopped")
                stop()

        except KeyboardInterrupt:
            logging.info("Bot has been aborted")
            stop()
        except BotAi.RestException as ex:
            if ex.name == 'GAME_NOT_STARTED':
                logging.info("Game has been stopped")
                stop()
            else:
                raise
