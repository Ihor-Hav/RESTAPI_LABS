from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[int] = None
    author: str
    title: str
