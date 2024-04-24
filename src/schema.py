from pydantic import BaseModel


class Entry(BaseModel):
    url: str
