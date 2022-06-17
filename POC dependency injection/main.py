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
    memory = Memory()
    memory.add({'pk': 1, 'name': 'John'})

    persistent = Persistent()
    persistent.add({'pk': 1, 'name': 'Jane'})

    print_storage_content(memory, 1)
    print_storage_content(persistent, 1)

    write_data(FileWriter(), "Hello world!")
