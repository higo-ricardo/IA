from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable


class StorageClient(ABC):
    """Contrato base para clientes de armazenamento."""

    @abstractmethod
    def put(self, key: str, payload: bytes) -> None:
        raise NotImplementedError


@dataclass
class MemoryStorage(StorageClient):
    db: dict[str, bytes]

    def put(self, key: str, payload: bytes) -> None:
        if not key:
            raise ValueError('key must not be empty')
        self.db[key] = payload


def seed(client: StorageClient, items: Iterable[tuple[str, bytes]]) -> None:
    for key, payload in items:
        client.put(key, payload)


if __name__ == '__main__':
    memory = MemoryStorage(db={})
    seed(memory, [('a', b'1'), ('b', b'2')])
    print(memory.db)
