import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK
from starlette.staticfiles import StaticFiles
from queue import SimpleQueue
import time

client_queues = []
app = FastAPI()


@app.get("/")
async def get():
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    with open("index.html") as file:
        html_read = file.read()
    return HTMLResponse(html_read)


@app.get("/data")
async def get():
    for queue in client_queues:
        queue.put({'name' : 'bot1'}, False)
        queue.put(, False)
    return len(client_queues)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    queue = SimpleQueue()
    client_queues.append(queue)
    data_send = {}
    await websocket.send_json(GameManager().map.data)
    while !GameManager().is_game_started:
        await asyncio.sleep(1)
    while websocket.client_state == websockets.WebSocketState.CONNECTED:
        try:
            timer = time.time()
            while time.time() - timer > 100:
                data = queue.get()
                data_send[data.pop('name')] = data
            await websocket.send_json(data_send)
            # await asyncio.sleep(1)
        except ConnectionClosedOK:
            break
    client_queues.remove(queue)
