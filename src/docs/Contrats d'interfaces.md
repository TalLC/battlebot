
- [Rest](#rest)
  - [`PATCH /display/clients/action/ready`](#patch-displayclientsactionready)
  - [`POST /bots/action/register`](#post-botsactionregister)
  - [`GET /bots/{bot_id}/action/request_connection`](#get-botsbot_idactionrequest_connection)
  - [`PATCH /bots/{bot_id}/action/check_connection`](#patch-botsbot_idactioncheck_connection)
  - [`PATCH /bots/{bot_id}/action/shoot`](#patch-botsbot_idactionshoot)
  - [`PATCH /bots/{bot_id}/action/turn`](#patch-botsbot_idactionturn)
  - [`PATCH /bots/{bot_id}/action/move`](#patch-botsbot_idactionmove)
- [MQTT](#mqtt)
  - [ServerMqttIdMessage](#servermqttidmessage)
  - [BotScannerDetectionMessage](#botscannerdetectionmessage)
- [STOMP](#stomp)
  - [ServerStompIdMessage](#serverstompidmessage)
  - [GameStatusMessage](#gamestatusmessage)
  - [BotHealthStatusMessage](#bothealthstatusmessage)
  - [BotStunningStatusMessage](#botstunningstatusmessage)
  - [BotMovingStatusMessage](#botmovingstatusmessage)
  - [BotTurningStatusMessage](#botturningstatusmessage)
  - [BotWeaponStatusMessage](#botweaponstatusmessage)


# Rest

Voici les endpoints disponibles via l'API Rest.

## `PATCH /display/clients/action/ready`
Définir le client d'affichage comme prêt si les jetons correspondent.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données d'identification de connexion",
    "type": "object",
    "required": [
        "login_id"
    ],
    "properties": {
        "login_id": {
            "type": "string",
            "description": "L'identifiant de connexion du client."
        }
    },
    "examples": [{
        "login_id": "551ef811-d241-40f8-8de4-3600ce73aee9"
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse de validation de jeton",
    "type": "object",
    "required": [
        "status",
        "message"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "L'état de l'opération de validation du jeton.",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Un message qui décrit le résultat de l'opération de validation du jeton.",
            "const": "Tokens are matching"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "Tokens are matching"
    }]
}
```


## `POST /bots/action/register`
Crée un nouvel objet bot et l'ajoute à l'équipe spécifiée.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données d'enregistrement du bot",
    "type": "object",
    "required": [
        "team_id",
        "bot_name"
    ],
    "properties": {
        "team_id": {
            "type": "string",
            "description": "L'ID de l'équipe à laquelle le bot doit être ajouté."
        },
        "bot_name": {
            "type": "string",
            "description": "Le nom du bot."
        }
    },
    "examples": [{
        "team_id": "given-team-id",
        "bot_name": "MyBot"
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse d'enregistrement du bot",
    "type": "object",
    "required": [
        "status",
        "message",
        "bot_id"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Le statut de l'opération d'enregistrement du bot.",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Un message qui décrit le résultat de l'opération d'enregistrement du bot.",
            "const": "The bot has been successfully registered"
        },
        "bot_id": {
            "type": "string",
            "description": "L'ID du bot enregistré."
        }
    },
    "examples": [{
        "status": "ok",
        "message": "The bot has been successfully registered",
        "bot_id": "ed758294-5d3e-4f4b-bad3-ab95839eb9de"
    }]
}
```


## `GET /bots/{bot_id}/action/request_connection`
Demande des IDs de connexion pour valider la connexion à tous les services. Envoie 3 IDs au client en utilisant REST, STOMP et MQTT. Le client doit renvoyer ces IDs sur l'endpoint `/bots/{bot_id}/action/check_connection` pour valider la connexion.

### Path parameters
| Nom | Description |
| --- | ----------- |
| bot_id | L'ID du bot qui demande une connexion |

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse de validation de connexion",
    "type": "object",
    "required": [
        "status",
        "message",
        "request_id"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut de la validation de connexion",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Un message qui indique que les ID MQTT et STOMP ont été dispatchés.",
            "const": "Messages sent from STOMP and MQTT"
        },
        "request_id": {
            "type": "string",
            "description": "ID Rest pour la validation de la connexion"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "Messages sent from STOMP and MQTT",
        "request_id": "0b5b9041-8bf0-45f2-a824-9d34e6a1c327"
    }]
}
```


## `PATCH /bots/{bot_id}/action/check_connection`
Vérifie si les IDs trouvés par le client sont ceux attendus pour valider la connexion du client à tous les services.

### Path parameters
| Nom | Description |
| --- | ----------- |
| bot_id | L'ID du robot à connecter |

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de connexion",
    "type": "object",
    "required": [
        "rest_id",
        "stomp_id",
        "mqtt_id"
    ],
    "properties": {
        "rest_id": {
            "type": "string",
            "description": "L'ID REST fourni par le client."
        },
        "stomp_id": {
            "type": "string",
            "description": "L'ID STOMP fourni par le client."
        },
        "mqtt_id": {
            "type": "string",
            "description": "L'ID MQTT fourni par le client."
        }
    },
    "examples": [
        {
            "rest_id": "0b5b9041-8bf0-45f2-a824-9d34e6a1c327",
            "stomp_id": "3ac537f1-88f5-4c97-bfb8-2cfdf2f89e92",
            "mqtt_id": "4242a3a5-3f4b-4e1f-bb4b-18d33f261d56"
        }
    ]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse à la connexion du bot",
    "type": "object",
    "required": [
        "status",
        "message"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Le statut de l'opération de connexion du bot.",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Un message qui décrit le résultat de l'opération de connexion du bot.",
            "const": "Your bot is successfully connected"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "Your bot is successfully connected"
    }]
}
```


## `PATCH /bots/{bot_id}/action/shoot`
Fait tirer le robot à l'angle relatif désiré.

### Path parameters
| Nom | Description |
| ---- | ----------- |
| bot_id | L'ID du robot qui doit tirer |

### Payload
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Données de tir du bot",
  "type": "object",
  "required": [
    "angle"
  ],
  "properties": {
    "angle": {
      "type": "int",
      "description": "L'angle auquel le robot doit tirer, en degrés."
    }
  },
  "examples": [
    {
      "angle": 42
    }
  ]
}
```

### Return
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Réponse de tir du bot",
  "type": "object",
  "required": [
    "status",
    "message"
  ],
  "properties": {
    "status": {
      "type": "string",
      "description": "Le statut de l'opération de tir du robot.",
      "const": "ok"
    },
    "message": {
      "type": "string",
      "description": "Un message qui décrit l'angle auquel le robot a tiré.",
      "const": "Fired at {angle}°"
    }
  },
  "examples": [
    {
      "status": "ok",
      "message": "Fired at 42°"
    }
  ]
}
```


## `PATCH /bots/{bot_id}/action/turn`
Commence à faire tourner le robot spécifié vers la gauche ou la droite.

### Path parameters
| Nom | Description |
| ---- | ----------- |
| bot_id | L'ID du robot à faire tourner |

### Payload
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Données de rotation du bot",
  "type": "object",
  "required": [
    "direction"
  ],
  "properties": {
    "direction": {
      "type": "string",
      "description": "La direction dans laquelle faire tourner le robot. Les valeurs valides sont 'left', 'right' et 'stop'"
    }
  },
  "examples": [
    {
      "direction": "left"
    }
  ]
}
```

### Return
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Réponse de rotation du bot",
  "type": "object",
  "required": [
    "status",
    "message"
  ],
  "properties": {
    "status": {
      "type": "string",
      "description": "Le statut de l'opération de rotation du robot.",
      "const": "ok"
    },
    "message": {
      "type": "string",
      "description": "Un message qui décrit la rotation demandée.",
      "const": "^Bot is starting to turn (left|right|stop)$"
    }
  },
  "examples": [
    {
      "status": "ok",
      "message": "Bot is starting to turn left"
    }
  ]
}
```


## `PATCH /bots/{bot_id}/action/move`
Commence à déplacer le robot spécifié vers l'avant.

### Path parameters
| Nom | Description |
| ---- | ----------- |
| bot_id | L'ID du robot à faire bouger |

### Payload
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Données de déplacement du bot",
  "type": "object",
  "required": [
    "action"
  ],
  "properties": {
    "action": {
      "type": "string",
      "description": "Ordre de déplacement du robot. Les valeurs valides sont 'start' et 'stop'"
    }
  },
  "examples": [
    {
      "action": "start"
    }
  ]
}
```

### Return
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Réponse de déplacement du bot",
  "type": "object",
  "required": [
    "status",
    "message"
  ],
  "properties": {
    "status": {
      "type": "string",
      "description": "Le statut de l'opération de déplacement du robot.",
      "const": "ok"
    },
    "message": {
      "type": "string",
      "description": "Un message qui décrit le déplacement demandé."
    }
  },
  "examples": [
    {
      "status": "ok",
      "message": "Bot is starting to move"
    },
    {
      "status": "ok",
      "message": "Bot has stopped moving"
    }
  ]
}
```


# MQTT

Voici les messages reçus par le client sur la file de messages MQTT. MQTT est seulement utilisé pour recevoir des messages de ce que le bot a dans son champs de vision.

## ServerMqttIdMessage

Identifiant envoyé au client pour valider le fonctionnement de la connexion à MQTT. Cet identifiant est à renvoyer au serveur via l'API Rest.

  * Queue: **BATTLEBOT/BOT/{bot_id}**
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
            "const": "mqtt_id"
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
                    "description": "The mqtt id to return using Rest",
                    "type": "str"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "mqtt_id",
        "source": "server",
        "data": {
            "value": "4242a3a5-3f4b-4e1f-bb4b-18d33f261d56"
        }
    }]
}
```

## BotScannerDetectionMessage

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


# STOMP

Voici les messages reçus par le client sur la file de messages STOMP. STOMP est utilisé pour recevoir les messages du jeu ou sur ce qui arrive au bot (perte de PV, arrêt, etc.).

## ServerStompIdMessage

Identifiant envoyé au client pour valider le fonctionnement de la connexion à STOMP. Cet identifiant est à renvoyer au serveur via l'API Rest.

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
            "const": "stomp_id"
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
                    "description": "The stomp id to return using Rest",
                    "type": "str"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "stomp_id",
        "source": "server",
        "data": {
            "value": "3ac537f1-88f5-4c97-bfb8-2cfdf2f89e92"
        }
    }]
}
```

## GameStatusMessage

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
                    "description": "Wether the game is started or not",
                    "type": "boolean",
                    "default": false
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

## BotHealthStatusMessage

Donne le nombre de PV du bot.

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
            "const": "health_status",
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
                    "description": "Bot HP",
                    "type": "int"
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
    }]
}
```

## BotStunningStatusMessage

État d'étourdissement du bot.

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
            "const": "stunning_status",
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
                    "description": "Is the bot stunned?",
                    "type": "bool"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "stunning_status",
        "source": "bot",
        "data": {
            "value": true
        }
    }]
}
```

## BotMovingStatusMessage

État de déplacement du bot.

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
            "const": "moving_status",
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
                    "description": "Is the bot moving?",
                    "type": "bool"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "moving_status",
        "source": "bot",
        "data": {
            "value": true
        }
    }]
}
```

## BotTurningStatusMessage

État de rotation du bot.

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
            "const": "turning_status",
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
                    "description": "Direction of the rotation",
                    "type": "str"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "turning_status",
        "source": "bot",
        "data": {
            "value": "left"
        }
    },
    {
        "msg_type": "turning_status",
        "source": "bot",
        "data": {
            "value": "right"
        }
    },
    {
        "msg_type": "turning_status",
        "source": "bot",
        "data": {
            "value": "stop"
        }
    }]
}
```

## BotWeaponStatusMessage

État de l'arme du bot.

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
            "const": "weapon_can_shoot",
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
                    "description": "Can the weapon shoot?",
                    "type": "bool"
                }
            }
        }
    },
    "examples": [{
        "msg_type": "weapon_can_shoot",
        "source": "bot",
        "data": {
            "value": true
        }
    }]
}
```
