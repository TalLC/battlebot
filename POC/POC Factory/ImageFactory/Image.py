from abc import abstractmethod, ABC


class Image(ABC):

    __filename: str

    @property
    def filename(self) -> str:
        return self.__filename

    def __init__(self, filename: str):
        self.__filename = filename

    def __str__(self):
        return f"Image {self.__filename}"

    @abstractmethod
    def load_image(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_image(self) -> None:
        raise NotImplementedError


class ImagePng(Image):

    def __init__(self, filename: str):
        super().__init__(filename)

    def load_image(self) -> None:
        print(f"Loading PNG image {self.filename}")

    def save_image(self) -> None:
        print(f"Saving PNG image {self.filename}")


class ImageGif(Image):

    def __init__(self, filename: str):
        super().__init__(filename)

    def load_image(self) -> None:
        print(f"Loading GIF image {self.filename}")

    def save_image(self) -> None:
        print(f"Saving GIF image {self.filename}")


class ImageJpg(Image):

    def __init__(self, filename: str):
        super().__init__(filename)

    def load_image(self) -> None:
        print(f"Loading JPG image {self.filename}")

    def save_image(self) -> None:
        print(f"Saving JPG image {self.filename}")
