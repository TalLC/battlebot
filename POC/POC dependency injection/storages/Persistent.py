from .Storage import Storage


class Persistent(Storage):
    items = []

    def add(self, item: dict):
        self.items.append(item)

    def get(self, pk: int) -> dict:
        for item in self.items:
            if item['pk'] == pk:
                return item
