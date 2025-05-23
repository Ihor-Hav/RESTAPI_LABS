from flask import Blueprint, request, jsonify, abort
from .models import Book
from . import db


books_bp = Blueprint('books', __name__)


@books_bp.route('/books', methods=['GET'])
def get_books():
    try:
        limit = int(request.args.get('limit', 10))
        cursor = request.args.get('cursor', None)
    except ValueError:
        return jsonify({"error": "limit must be an integer"}), 400

    if limit > 100:
        limit = 100
    if limit < 1:
        return jsonify({"error": "limit must be > 0"}), 400

    query = Book.query.order_by(Book.id.asc())

    if cursor:
        try:
            cursor_id = int(cursor)
            query = query.filter(Book.id > cursor_id)
        except ValueError:
            return jsonify({"error": "cursor must be an integer"}), 400

    books = query.limit(limit + 1).all()  # get 1 extra to check if there's a next page

    has_next = len(books) > limit
    books = books[:limit]

    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author
        })

    response = {
        "limit": limit,
        "count": len(result),
        "books": result,
        "next_cursor": books[-1].id if has_next else None
    }

    return jsonify(response), 200



@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404, description="Book not found")

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author
    }), 200



@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')

    new_book = Book(title=title, author=author)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author
    }), 201


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404, description="Book not found")

    db.session.delete(book)
    db.session.commit()

    return jsonify({"status": "success"}), 200