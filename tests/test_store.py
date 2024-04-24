import pytest

from src.db import DBStore
from src.main import hasher
from src.schema import Entry
from src.store import MemStore, Store


# non trivial fixture matrix needed here
@pytest.mark.parametrize(
    "store",
    [(MemStore(key=hasher)), (DBStore(key=hasher, db_file="tests/.test-slug.db"))],
    ids=["mem", "db"],
)
class TestStore:

    def test_write_read(self, store: Store):
        # write and read it
        entry = Entry(url="https://google.com")
        slug = store.insert(entry)
        assert store.get(slug) == entry

    def test_write_twice(self, store):
        # same url should give a different slug each time
        entry = Entry(url="https://url.com")
        slug = store.insert(entry)
        snail = store.insert(entry)
        assert store.get(slug) == entry
        assert store.get(snail) == entry
        assert slug != snail

    def test_read_error(self, store: Store):
        # read something that does not exist and get error
        slug = "abcde"
        assert store.get(slug) is None
