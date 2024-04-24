import os
import sqlite3
from dataclasses import dataclass
from typing import Optional, Iterable

from store import Store
from schema import Entry


DB_FILE = "slug.db"
TABLE = "slug"
CREATE_DB = f"""
CREATE TABLE {TABLE}(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    key VARCHAR(255) UNIQUE NOT NULL,
    url TEXT
)
"""

@dataclass
class DBStore(Store):

    def __post_init__(self):
        # check db exists or initialize it
        if not os.path.exists(DB_FILE):
            self.connect().cursor().execute(CREATE_DB)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(DB_FILE)

    def get(self, key: str) -> Optional[Entry]:
        result = self.connect().cursor().execute(
            f"""
            SELECT *
            FROM {TABLE}
            WHERE key = ?
            """,
            (key,)
        )
        ans = result.fetchone()
        if ans is None:
            return ans
        _id, _key, url = ans
        return Entry(
            url=url,
        )

    def insert(self, entry: Entry) -> str:
        key = self.key(entry)
        con = self.connect()
        con.cursor().execute(
            f"""
            INSERT INTO {TABLE} (key, url)
            VALUES (?, ?)
            """,
            (key, entry.url),
        )
        con.commit()
        return key
    
    def list(self) -> Iterable[tuple[str, Entry]]:
        return (
            (key, Entry(url=url))
            for id, key, url in 
            self.connect().cursor().execute(
            f"""
            SELECT * FROM {TABLE}
            """
        ).fetchall())
