import math
import random
from time import sleep

import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()


@app.get("/")
async def get():
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    with open("index.html") as file:
        html_read = file.read()
    print(html_read)
    return HTMLResponse(html_read)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    liste_event = [
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 0,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 8,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 10,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 8,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 2,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -4,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 8,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": 0,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -6,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -4,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -2,
            "rotateX": 0.0,
            "rotateY": math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -4,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": -2,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 0,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 2,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 4,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0
        },
        {
            "name": "bot1",
            "x": 6,
            "y": 0,
            "z": -6,
            "rotateX": 0.0,
            "rotateY": -math.pi / 2,
            "rotateZ": 0.0
        }
    ]

    await websocket.accept()
    while True:
        for value in liste_event:
            sleep(1)
            await websocket.send_json(value)
