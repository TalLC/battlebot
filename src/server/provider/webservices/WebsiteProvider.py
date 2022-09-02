import logging
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI


class WebsiteProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_page_root()
        self.__register_page_test_ws_data()

    def __register_page_root(self):
        @self.__app.get("/")
        async def get():
            self.__app.mount("/static", StaticFiles(directory="www/static"), name="static")
            with open("www/index.html") as file:
                html_read = file.read()
            return HTMLResponse(html_read)

    def __register_page_test_ws_data(self):
        @self.__app.get("/data")
        async def get():
            return "TO_DEFINE"
            # for queue in client_queues:
            #     queue.put({'name': 'bot1'}, False)
            #     return len(client_queues)
