from provider.webservices.rest.models.AdminBaseModel import AdminBaseModel


class AdminActionBanModel(AdminBaseModel):
    host: str
    source: str
    reason: str
    definitive: bool
