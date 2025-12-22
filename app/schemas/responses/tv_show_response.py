from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class TVShowResponse(BaseModel):
    id: int
    url: HttpUrl
    name: str
    type: str
    language: str
    genres: Optional[List[str]] = []
    status: str
    runtime: Optional[int] = None