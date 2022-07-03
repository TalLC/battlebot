from Image import Image, ImagePng, ImageGif, ImageJpg
from ImageFactory import ImageFactory


class ImageFactoryImpl(ImageFactory):

    def create_image(self, filename: str) -> Image:
        image: Image
        if filename.endswith(".png"):
            image = ImagePng(filename)
        elif filename.endswith(".gif"):
            image = ImageGif(filename)
        elif filename.endswith(".jpg"):
            image = ImageJpg(filename)
        else:
            raise Exception(f"Unknown image type: {filename}")

        image.load_image()
        return image
