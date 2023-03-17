from pydantic import BaseModel


class AdminBaseModel(BaseModel):
    api_password: str
