from Singleton import SingletonABCMeta
from Image import Image
from abc import abstractmethod, ABC


class ImageFactory(ABC, metaclass=SingletonABCMeta):

        @abstractmethod
        def create_image(self, filename: str) -> Image:
            raise NotImplementedError
