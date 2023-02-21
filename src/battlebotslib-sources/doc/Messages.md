# Messages

## MQTT

Voici les messages reçus par le client sur la file de messages MQTT. MQTT est seulement utilisé pour recevoir des messages de ce que le bot a dans son champs de vision.

### BotScannerDetectionMessage

Informations sur les objets détectés par le bot (type d'objet, distance, angle auquel ils se trouvent).

  * Queue: **BATTLEBOT/BOT/{bot_id}**
  * Producer: **server**
  * Consumer: **client**
  * Payload:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": [
        "source",
        "msg_type",
        "data"
    ],
    "properties": {
        "msg_type": {
            "description": "Type of information",
            "const": "object_detection"
        },
        "source": {
            "description": "Where does the information comes from",
            "const": "scanner"
        },
        "data": {
            "type": "array",
            "items": {
                "description": "Detected object(s)",
                "type": "object",
                "required": [
                    "from",
                    "to",
                    "object_type",
                    "name",
                    "distance"
                ],
                "properties": {
                    "from": {
                        "description": "Angle from which the object starts to be seen by the bot",
                        "type": "float"
                    },
                    "to": {
                        "description": "Angle from which the object is not visible anymore by the bot",
                        "type": "float"
                    },
                    "object_type": {
                        "description": "Type of the detected object",
                        "type": "string"
                    },
                    "name": {
                        "description": "Name of the detected object",
                        "type": "string"
                    },
                    "distance": {
                        "description": "Distance from the bot to the object",
                        "type": "float"
                    }
                }
            }
        }
    },
    "examples": [
        {
            "msg_type": "object_detection",
            "source": "scanner",
            "data": [
                {
                    "from": 26.5,
                    "to": 31,
                    "object_type": "tree",
                    "name": "Tree",
                    "distance": 6.844473640068633
                },
                {
                    "from": 34,
                    "to": 39.5,
                    "object_type": "bot",
                    "name": "MyBot01",
                    "distance": 5.777348380771669
                }
            ]
        }
    ]
}
```


## STOMP

Voici les messages reçus par le client sur la file de messages STOMP. STOMP est utilisé pour recevoir les messages du jeu ou sur ce qui arrive au bot (perte de PV, arrêt, etc.).

### GameStatusMessage

Informe le client du démarrage et de l'arrêt de la partie.

  * Queue: **BATTLEBOT.BOT.{bot_id}**
  * Producer: **server**
  * Consumer: **client**
  * Payload:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "required": [
        "msg_type",
        "source",
        "data"
    ],
    "properties": {
        "msg_type": {
            "description": "Type of information",
            "const": "game_status"
        },
        "source": {
            "description": "Where does the information comes from",
            "const": "server"
        },
        "data": {
            "type": "object",
            "required": [
                "value"
            ],
            "properties": {
                "value": {
                    "type": "boolean",
                    "default": false,
                    "description": "Wether the game is started or not"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "game_status",
        "source": "server",
        "data": {
            "value": false
        }
    }]
}
```

### IBotMessage

Donne des informations relatives à l'état du bot.

  * Queue: **BATTLEBOT.BOT.{bot_id}**
  * Producer: **server**
  * Consumer: **client**
  * Payload:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "required": [
        "msg_type",
        "source",
        "data"
    ],
    "properties": {
        "msg_type": {
            "description": "Type of information",
            "type": "string",
        },
        "source": {
            "description": "Where does the information comes from",
            "const": "bot"
        },
        "data": {
            "type": "object",
            "required": [
                "value"
            ],
            "properties": {
                "value": {
                    "type": "any",
                    "description": "Value corresponding to the type of information"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "health_status",
        "source": "bot",
        "data": {
            "value": 95
        }
    },
    {
        "msg_type": "stunning_status",
        "source": "bot",
        "data": {
            "value": true
        }
    },
    {
        "msg_type": "moving_status",
        "source": "bot",
        "data": {
            "value": false
        }
    },
    {
        "msg_type": "turning_status",
        "source": "bot",
        "data": {
            "value": false
        }
    },
    {
        "msg_type": "weapon_can_shoot",
        "source": "bot",
        "data": {
            "value": false
        }
    }]
}
```
