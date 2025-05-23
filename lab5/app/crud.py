from .database import books_collection
from bson import ObjectId
from fastapi import HTTPException


async def get_all_books():
    books_cursor = books_collection.find({})
    books = []
    async for book in books_cursor:
        book["_id"] = str(book["_id"])
        books.append(book)
    return books


async def get_book(book_id: str):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book["_id"] = str(book["_id"])
    return book


async def add_book(book_data: dict):
    result = await books_collection.insert_one(book_data)
    new_book = await books_collection.find_one({"_id": result.inserted_id})
    new_book["_id"] = str(new_book["_id"])
    return new_book


async def delete_book(book_id: str):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} deleted"}
