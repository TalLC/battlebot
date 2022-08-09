import math
import random
from time import sleep

import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

with open("./static/map/map.txt") as map:
    map_txt = map.read()

@app.get("/")
async def get():
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    with open("index.html") as file:
        html_read = file.read()
    return HTMLResponse(html_read)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    liste_event = [
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 0,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 8,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 8,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 2,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -4,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 0,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -4,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 2,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "type": "move",
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        }
    ]
    create_sol ={
            "type": "create",
            "name": "sol",
            "x": 0,
            "y": 0,
            "z": 0,
        }
    create_eau ={
            "type": "create",
            "name": "eau",
            "x": 0,
            "y": 0,
            "z": 0,
        }

    await websocket.accept()
    ligne = 0
    col = 0
    for v in map_txt:
        if v == 'S':
            create_sol['x'] = ligne * 2
            create_sol['z'] = col * 2
            await websocket.send_json(create_sol)
        elif v == 'E':
            create_eau['x'] = ligne * 2
            create_eau['z'] = col * 2
            await websocket.send_json(create_eau)
        elif v == '\n':
            col = -1
            ligne += 1
        col += 1

    while True:
        for value in liste_event:
            sleep(1)
            await websocket.send_json(value)
