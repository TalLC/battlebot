from provider.webservices.rest.models.AdminBaseModel import AdminBaseModel


class AdminDisplayClientsActionGetByTokenModel(AdminBaseModel):
    client_token: str
