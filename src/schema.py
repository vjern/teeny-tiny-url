from pydantic import BaseModel, field_validator


class Entry(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, url: str):
        if not url.strip():
            # Or use a off-the-shelf parser or a regex for more rigorous validation
            raise ValueError("Not an url")
        return url
