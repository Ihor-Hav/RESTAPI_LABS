from pydantic import BaseModel

class BookIn(BaseModel):
    title: str
    author: str

class Book(BookIn):
    _id: str

# New models for auth
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str
