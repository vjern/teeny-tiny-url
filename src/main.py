from datetime import datetime
from hashlib import sha256

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

from db import DBStore
from schema import Entry
from store import MemStore

app = FastAPI()


def hasher(entry: Entry) -> str:
    salt = str(datetime.now().timestamp())
    cache = sha256()
    cache.update(entry.url.encode())
    cache.update(salt.encode())
    return cache.hexdigest()[-8:]


store = DBStore(key=hasher)
# store = MemStore(key=hasher)


@app.get("/")
def liveness():
    return "teeny-tiny-url v0"


@app.post("/")
def register(body: Entry):
    return store.insert(body)


@app.get("/list")
def list():
    return store.list()


@app.get("/{key}")
def forward(key: str):
    entry = store.get(key)
    if entry is None:
        return PlainTextResponse(
            status_code=404,
            content="Not found",
        )
    return HTMLResponse(
        content=f"""
    <head>
        <meta http-equiv="Refresh" content="0 URL={entry.url}" />
    </head>
    """
    )
