from ImageFactoryImpl import ImageFactoryImpl

#
# ImageFactoryImpl est une classe qui implémente l'interface ImageFactory
# ImageFactory est un Singleton
#
# En fonction du nom de fichier donné en entrée, on crée une instance de Image correspondante
#


if __name__ == '__main__':

    # Chargement d'une image PNG et renvoi d'une instance de la classe ImagePng
    image_png = ImageFactoryImpl().create_image("image.png")

    # Chargement d'une image GIF et renvoi d'une instance de la classe ImageGif
    image_gif = ImageFactoryImpl().create_image("image.gif")

    # On vérifie que les objets sont bien créés
    print(image_png)
    print(image_gif)
