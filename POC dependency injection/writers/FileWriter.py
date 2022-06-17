from .Writer import Writer


class FileWriter(Writer):

    def write(self, data: str):
        print(f'Writing "{data}" to a file')

