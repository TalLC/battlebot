from storages.Storage import Storage
from storages.Memory import Memory
from storages.Persistent import Persistent

from writers.Writer import Writer
from writers.FileWriter import FileWriter


def print_storage_content(storage: Storage, primary_key: int):
    print(f"Stored content: {storage.get(primary_key)}")


def write_data(writer: Writer, data: str):
    writer.write(data)


if __name__ == "__main__":
    Memory().add({'pk': 1, 'name': 'John'})
    Memory().add({'pk': 2, 'name': 'John2'})
    Persistent().add({'pk': 1, 'name': 'Jane'})

    print_storage_content(Memory(), 1)
    print_storage_content(Memory(), 2)
    print_storage_content(Persistent(), 1)

    write_data(FileWriter(), "Hello world!")
