from fastapi.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI


class WebsiteProvider:
    tags_metadata = [
        {"name": "web", "description": "Battlebot website"},
    ]
    _favicon_path = 'www/favicon.ico'

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__app.openapi_tags += self.tags_metadata
        self.__register_page_root()
        self.__register_page_favicon()

    def __register_page_root(self):
        @self.__app.get("/", tags=['web'])
        async def get():
            """
            Battlebot main webpage.
            """
            self.__app.mount("/static", StaticFiles(directory="www/static"), name="static")
            with open("www/index.html", encoding="utf-8") as file:
                html_read = file.read()
            return HTMLResponse(html_read)

    def __register_page_favicon(self):
        @self.__app.get('/favicon.ico', include_in_schema=False)
        async def favicon():
            """
            Add a favicon.
            """
            return FileResponse(self._favicon_path)
