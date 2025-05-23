from flask import Blueprint, request, jsonify, abort
from .models import Book
from . import db


books_bp = Blueprint('books', __name__)


@books_bp.route('/books', methods=['GET'])
def get_books():
    # Отримуємо параметри limit і offset з query string, задаємо дефолтні значення
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"error": "limit and offset must be integers"}), 400

    # Обмеження на максимальний limit, щоб уникнути надмірного навантаження
    if limit > 100:
        limit = 100
    if limit < 1 or offset < 0:
        return jsonify({"error": "limit must be > 0 and offset >= 0"}), 400

    # Запит з пагінацією
    books = Book.query.limit(limit).offset(offset).all()

    if not books:
        return jsonify({"message": "No books found"}), 404

    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author
        })

    return jsonify({
        "limit": limit,
        "offset": offset,
        "count": len(result),
        "books": result
    }), 200



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