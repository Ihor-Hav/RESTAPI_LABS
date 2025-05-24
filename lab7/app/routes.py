from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from bson import ObjectId
from .database import books_collection
from .models import Book, BookIn
from .auth import get_current_user

router = APIRouter()


@router.get("/books")
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[str] = None,
    user: dict = Depends(get_current_user)  # 🔐 Protected endpoint
):
    query = {}
    if cursor:
        if not ObjectId.is_valid(cursor):
            raise HTTPException(status_code=400, detail="Invalid cursor ID")
        query["_id"] = {"$gt": ObjectId(cursor)}

    cursor_db = books_collection.find(query).sort("_id", 1).limit(limit + 1)
    books = await cursor_db.to_list(length=limit + 1)

    has_next = len(books) > limit
    books = books[:limit]

    for book in books:
        book["_id"] = str(book["_id"])

    response = {
        "limit": limit,
        "count": len(books),
        "books": books,
        "next_cursor": str(books[-1]["_id"]) if has_next else None
    }
    return response


@router.get("/books/{book_id}")
async def get_book(book_id: str, user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book["_id"] = str(book["_id"])
    return book


@router.post("/books", status_code=201)
async def add_book(book: BookIn, user: dict = Depends(get_current_user)):
    result = await books_collection.insert_one(book.dict())
    new_book = await books_collection.find_one({"_id": result.inserted_id})
    new_book["_id"] = str(new_book["_id"])
    return new_book


@router.delete("/books/{book_id}")
async def delete_book(book_id: str, user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "success"}
