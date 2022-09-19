from fastapi import WebSocket
from provider.security.NetworkSecurity import NetworkSecurity


def antispam_websocket(func):
    async def wrap(websocket: WebSocket):
        blacklisted = NetworkSecurity().update_ip(websocket.client.host, 'websocket')
        await websocket.accept()

        if blacklisted is None:
            await func(websocket)
        else:
            await websocket.send_json(blacklisted.light_json())
            await websocket.close()

    return wrap
