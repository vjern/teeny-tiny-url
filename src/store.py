from typing import Callable, Iterable
from dataclasses import dataclass, field

from schema import Entry


@dataclass
class Store:
    key: Callable[[Entry], str]

    def get(self, key: str) -> Entry:
        raise NotImplementedError

    def insert(self, entry: Entry) -> str:
        raise NotImplementedError

    def list(self) -> Iterable[tuple[str, Entry]]:
        raise NotImplementedError

@dataclass
class MemStore(Store):
    mem: dict[str, Entry] = field(default_factory=dict)

    def get(self, key):
        return self.mem.get(key)

    def insert(self, entry):
        key = self.key(entry)
        self.mem[key] = entry
        return key

    def list(self):
        return self.mem.items()
