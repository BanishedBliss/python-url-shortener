from pydantic import BaseModel, HttpUrl

# Модели Pydantic
class ShortenRequest(BaseModel):
    url: HttpUrl

class AsyncRequest(BaseModel):
    url: HttpUrl

class ShortenResponse(BaseModel):
    short_id: str

class AsyncResponse(BaseModel):
    status: int
    headers: dict
    content: str