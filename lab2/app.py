from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()


class Book(BaseModel):
    id: int = None
    author: str
    title: str


books = [
    {
        "id": 0,
        "author": "J.K. Rowling",
        "title": "Harry Potter and the Sorcerer's Stone"
    }
]


@app.get("/books", response_model=List[Book])
async def get_books():
    return books


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=Book)
async def add_book(book: Book):
    new_book = book.dict()
    new_book["id"] = len(books)
    books.append(new_book)
    return new_book


@app.delete("/books/{book_id}", status_code=200)
async def delete_book(book_id: int):
    global books
    books = [b for b in books if b["id"] != book_id]
    return {"message": "Book deleted"}
