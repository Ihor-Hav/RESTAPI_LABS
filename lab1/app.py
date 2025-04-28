from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)


books = [
    {
        "id": 0,
        "author": "J.K. Rowling",
        "title": "Harry Potter and the Sorcerer's Stone"
    }
]


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    author = fields.Str(required=True)
    title = fields.Str(required=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_schema.dump(books)), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book_schema.dump(book)), 200


@app.route('/books', methods=['POST'])
def add_book():
    try:

        new_book = book_schema.load(request.json)
        new_book["id"] = len(books)
        books.append(new_book)
        return jsonify(book_schema.dump(new_book)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200


@app.route('/')
def home():
    return '<h1>Flask Restful API</h1>'

if __name__ == "__main__":
    app.run(debug=True)
