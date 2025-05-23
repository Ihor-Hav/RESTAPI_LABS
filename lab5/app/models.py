from pydantic import BaseModel

class BookIn(BaseModel):
    title: str
    author: str

class Book(BookIn):
    _id: str
