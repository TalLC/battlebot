from functools import wraps
from fastapi import WebSocket, Request
from starlette import websockets
from common.config import CONFIG_NETWORK_SECURITY
from common.ErrorCode import ErrorCode, NETWORK_BANNED_IP_TEMP, NETWORK_BANNED_IP_DEF
from provider.security.NetworkSecurity import NetworkSecurity


class NetworkSecurityDecorators:

    @staticmethod
    def rest_ban_check(func):
        """
        Rest endpoint decorator. Check if the client is banned and allow or deny the call.
        """
        @wraps(func)
        async def wrap(*args, **kwargs):
            # Finding request object
            request = None
            banned_ip = None
            for value in kwargs.values():
                if isinstance(value, Request):
                    request = value
                    break

            # If we found the request...
            if request is not None:
                # fetching ban information about the client
                banned_ip = NetworkSecurity().get_ban_info_for_ip(request.client.host, 'rest')

            # If the client is not banned, we can continue
            if banned_ip is None:
                return await func(*args, **kwargs)
            else:
                # else, we send ban information over Rest
                if banned_ip.definitive:
                    ErrorCode.throw(NETWORK_BANNED_IP_DEF)
                else:
                    ErrorCode.throw(NETWORK_BANNED_IP_TEMP)

        return wrap

    @staticmethod
    def websocket_ban_check(func):
        """
        Websocket endpoint decorator. Check if the client is banned and allow or deny the call.
        """
        @wraps(func)
        async def wrap(*args, **kwargs):
            # Finding websocket object
            websocket = None
            for value in kwargs.values():
                if isinstance(value, WebSocket):
                    websocket = value
                    break

            # If we found the websocket...
            if websocket is not None:
                # we accept the connection if needed
                if websocket.client_state == websockets.WebSocketState.CONNECTING:
                    await websocket.accept()

                # Ensuring the connection is established between client and server
                if websocket.client_state == websockets.WebSocketState.CONNECTED:
                    # Fetching ban information about the client
                    banned_ip = NetworkSecurity().get_ban_info_for_ip(websocket.client.host, 'websocket')

                    # If the client is not banned, we can continue
                    if banned_ip is None:
                        return await func(*args, **kwargs)
                    else:
                        # else, we send ban information over websocket and abort the connection
                        await websocket.send_json(banned_ip.light_json())
                        await websocket.close()

        return wrap

    @staticmethod
    def websocket_autoban(func):
        """
        Websocket endpoint decorator. Auto-ban the client if he is spamming the service.
        """
        @wraps(func)
        async def wrap(*args, **kwargs):
            # Finding websocket object
            websocket = None
            for value in kwargs.values():
                if isinstance(value, WebSocket):
                    websocket = value
                    break

            # If we found the websocket...
            if websocket is not None:
                # we accept the connection if needed
                if websocket.client_state == websockets.WebSocketState.CONNECTING:
                    await websocket.accept()

                # Ensuring the connection is established between client and server
                if websocket.client_state == websockets.WebSocketState.CONNECTED:
                    # Bypassing auto ban if disabled
                    if not CONFIG_NETWORK_SECURITY.enable_auto_ban:
                        return await func(*args, **kwargs)
                    else:
                        # Updating login information about the client and checking if it is currently
                        # spamming the websocket
                        banned_ip = NetworkSecurity().update_ip(websocket.client.host, 'websocket')

                        # If the client is not banned, we can continue
                        if banned_ip is None:
                            return await func(*args, **kwargs)
                        else:
                            # else, we send ban information over websocket and abort the connection
                            await websocket.send_json(banned_ip.light_json())
                            await websocket.close()

        return wrap
