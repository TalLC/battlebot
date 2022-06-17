from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class ApiMockExample:
    def __init__(self):
        self.api = 'api_mock'

    def get_api(self):
        return self.api


class ApiExample:
    def __init__(self):
        self.api = 'api'

    def get_api(self):
        return self.api


class ServiceExample:
    def __init__(self):
        self.service = 'service'

    def get_service(self):
        return self.service


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    api_client = providers.Singleton(ApiExample, api_key=config.api_key, timeout=config.timeout)
    service = providers.Factory(ServiceExample, api_client=api_client)


@inject
def main(service: ServiceExample = Provide[Container.service]):
    print(service.get_service())


if __name__ == "__main__":
    container = Container()
    container.config.api_key.from_env("API_KEY", required=True)
    container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
    container.wire(modules=[__name__])

    main()  # <-- dependency is injected automatically

    with container.api_client.override(ApiMockExample()):
        main()  # <-- overridden dependency is injected automatically
