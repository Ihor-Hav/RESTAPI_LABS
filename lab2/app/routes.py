from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Book
from app.data import books, generate_new_id

router = APIRouter()


@router.get("/books", response_model=List[Book])
async def get_books():
    return books


@router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/books", response_model=Book, status_code=201)
async def add_book(book: Book):
    new_book = book.dict()
    new_book["id"] = generate_new_id()
    books.append(new_book)
    return new_book


@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books.remove(book)
    return
