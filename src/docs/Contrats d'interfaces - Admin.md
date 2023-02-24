
- [Rest](#rest)
  - [`POST /admin/action/ban`](#post-adminactionban)
  - [`PATCH /admin/action/unban`](#patch-adminactionunban)
  - [`PATCH /game/action/start`](#patch-gameactionstart)
  - [`PATCH /game/action/select_map`](#patch-gameactionselect_map)
  - [`GET /display/clients/action/list`](#get-displayclientsactionlist)
  - [`GET /display/clients/action/get_by_id`](#get-displayclientsactionget_by_id)
  - [`GET /display/clients/action/get_by_token`](#get-displayclientsactionget_by_token)
  - [`PATCH /bots/action/add`](#patch-botsactionadd)
  - [`PATCH /bots/{bot_id}/action/kill`](#patch-botsbot_idactionkill)


# Rest

## `POST /admin/action/ban`
Bannir l'adresse IP spécifiée d'une source spécifique.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de banissement",
    "type": "object",
    "required": [
        "api_password",
        "host",
        "source",
        "reason",
        "definitive"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        },
        "host": {
            "type": "string",
            "description": "IP à bannir"
        },
        "source": {
            "type": "string",
            "description": "Source dont on veut ban l'IP"
        },
        "reason": {
            "type": "string",
            "description": "Raison du ban"
        },
        "definitive": {
            "type": "bool",
            "description": "Banissement définitif ou temporaire avec déban automatique ?"
        }
    },
    "examples": [{
        "api_password": "password",
        "host": "10.0.0.2",
        "source": "rest",
        "reason": "Tricherie",
        "definitive": true
    },
    {
        "api_password": "password",
        "host": "10.0.0.3",
        "source": "websocket",
        "reason": "Too many connections in a short delay",
        "definitive": false
    }]
}
```


### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse au banissement",
    "type": "object",
    "required": [
        "status",
        "banned"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "banned": {
            "type": "string",
            "description": "Adresse IP bannie"
        }
    },
    "examples": [{
        "status": "ok",
        "banned": "10.0.0.2"
    }]
}
```


## `PATCH /admin/action/unban`
Débannir l'adresse IP spécifiée pour une source spécifique.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de débanissement",
    "type": "object",
    "required": [
        "api_password",
        "host",
        "source"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        },
        "host": {
            "type": "string",
            "description": "IP à débannir"
        },
        "source": {
            "type": "string",
            "description": "Source dont on veut déban l'IP"
        }
    },
    "examples": [{
        "api_password": "password",
        "host": "10.0.0.2",
        "source": "rest"
    }]
}
```


### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse au débanissement",
    "type": "object",
    "required": [
        "status",
        "message"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Adresse IP débannie"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "10.0.0.2 unbanned"
    }]
}
```


## `PATCH /game/action/start`
Démarrer la partie en cours.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données d'identification admin",
    "type": "object",
    "required": [
        "api_password"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        }
    },
    "examples": [{
        "api_password": "password"
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse au démarrage de la partie",
    "type": "object",
    "required": [
        "status",
        "message"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Etat de la partie",
            "const": "Game is started"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "Game is started"
    }]
}
```


## `PATCH /game/action/select_map`
Sélectionner la carte.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de changement de map",
    "type": "object",
    "required": [
        "api_password",
        "map_name"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        },
        "map_name": {
            "type": "string",
            "description": "Nom de la map à charger"
        }
    },
    "examples": [{
        "api_password": "password",
        "map_name": "test_map_16_16"
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse au changement de map",
    "type": "object",
    "required": [
        "status",
        "message"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Etat du chargement de la map",
            "const": "Map is loaded."
        }
    },
    "examples": [{
        "status": "ok",
        "message": "Map is loaded."
    }]
}
```


## `GET /display/clients/action/list`
Retourne des informations sur les clients d'affichage présents et passés.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de recherche des clients web",
    "type": "object",
    "required": [
        "api_password",
        "connected_only"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        },
        "connected_only": {
            "type": "bool",
            "description": "Ne rechercher que les client connectés actuellement"
        }
    },
    "examples": [{
        "api_password": "password",
        "connected_only": true
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse à la récupération des clients web",
    "type": "object",
    "required": [
        "status",
        "clients"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "clients": {
            "type": "list",
            "description": "Liste des objets clients trouvés"
        }
    },
    "examples": [{
        "status": "ok",
        "clients": [
          {}
        ]
    }]
}
```


## `GET /display/clients/action/get_by_id`
Trouve un client d'affichage par son ID.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de recherche de client web",
    "type": "object",
    "required": [
        "api_password",
        "client_id"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        },
        "client_id": {
            "type": "integer",
            "description": "ID du client à rechercher"
        }
    },
    "examples": [{
        "api_password": "password",
        "client_id": 1
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse à la récupération du client web",
    "type": "object",
    "required": [
        "status",
        "client"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "client": {
            "type": "object",
            "description": "Objet client trouvé"
        }
    },
    "examples": [{
        "status": "ok",
        "client": {}
    }]
}
```


## `GET /display/clients/action/get_by_token`

Trouve un client d'affichage par son token.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données de recherche de client web",
    "type": "object",
    "required": [
        "api_password",
        "client_token"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        },
        "client_token": {
            "type": "string",
            "description": "Token du client à rechercher"
        }
    },
    "examples": [{
        "api_password": "password",
        "client_token": "688c14bd-4b0a-414e-b037-ebf35080642b"
    }]
}
```


### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse à la récupération du client web",
    "type": "object",
    "required": [
        "status",
        "client"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "client": {
            "type": "object",
            "description": "Objet client trouvé"
        }
    },
    "examples": [{
        "status": "ok",
        "client": {}
    }]
}
```


## `PATCH /bots/action/add`
Ajoute un bot sans IA dans le jeu.

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données d'identification admin",
    "type": "object",
    "required": [
        "api_password"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        }
    },
    "examples": [{
        "api_password": "password"
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse à l'ajout de bot",
    "type": "object",
    "required": [
        "status",
        "message",
        "bot_id"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Etat de l'ajout du bot",
            "const": "The bot has been added"
        },
        "bot_id": {
            "type": "string",
            "description": "ID du bot ajouté"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "The bot has been added",
        "bot_id": "a78e716a-315b-435d-b36c-fa4c7410ea26"
    }]
}
```


## `PATCH /bots/{bot_id}/action/kill`
Tue le bot spécifié.

### Path parameters
| Nom | Description |
| --- | ----------- |
| bot_id | L'ID du bot à tuer |

### Payload
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Données d'identification admin",
    "type": "object",
    "required": [
        "api_password"
    ],
    "properties": {
        "api_password": {
            "type": "string",
            "description": "Mot de passe admin Rest"
        }
    },
    "examples": [{
        "api_password": "password"
    }]
}
```

### Return
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Réponse au kill de bot",
    "type": "object",
    "required": [
        "status",
        "message",
        "bot_id"
    ],
    "properties": {
        "status": {
            "type": "string",
            "description": "Statut du traitement de la demande",
            "const": "ok"
        },
        "message": {
            "type": "string",
            "description": "Etat de l'opération",
            "const": "The bot has been killed"
        },
        "bot_id": {
            "type": "string",
            "description": "ID du bot tué"
        }
    },
    "examples": [{
        "status": "ok",
        "message": "The bot has been killed",
        "bot_id": "a78e716a-315b-435d-b36c-fa4c7410ea26"
    }]
}
```
