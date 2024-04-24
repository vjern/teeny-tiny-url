import re

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse

from schema import Entry
from store import MemStore

app = FastAPI()

i = 0
def hasher(entry: Entry) -> str:
    global i
    i += 1
    return str(i)

store = MemStore(key=hasher)


@app.get("/")
def liveness():
    return "teeny-tiny-url v0"


@app.post("/")
def register(body: Entry):
    return store.insert(body)


@app.get("/{key}")
def forward(key: str):
    entry = store.get(key)
    if entry is None:
        return PlainTextResponse(
            status_code=404,
            content='Not found', 
        )
    return HTMLResponse(
        content=entry.url
    )
