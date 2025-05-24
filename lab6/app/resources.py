from flask import request
from flask_restful import Resource
from flasgger import swag_from
from .models import Book
from . import db


class BookListResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'List of books',
                'examples': {
                    'application/json': {
                        'count': 1,
                        'books': [
                            {'id': 1, 'title': '1984', 'author': 'Orwell'}
                        ]
                    }
                }
            }
        },
        'parameters': [
            {
                'name': 'limit',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 10
            },
            {
                'name': 'offset',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 0
            }
        ]
    })
    def get(self):
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))

        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)

        books = Book.query.limit(limit).offset(offset).all()

        result = [{"id": b.id, "title": b.title, "author": b.author} for b in books]

        return {
            "count": len(result),
            "books": result
        }, 200

    @swag_from({
        'responses': {
            201: {
                'description': 'Book created',
                'examples': {
                    'application/json': {
                        'id': 1,
                        'title': 'New Book',
                        'author': 'Author Name'
                    }
                }
            }
        },
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'author': {'type': 'string'}
                    },
                    'required': ['title', 'author']
                }
            }
        ]
    })
    def post(self):
        data = request.get_json()
        book = Book(title=data['title'], author=data['author'])

        db.session.add(book)
        db.session.commit()

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author
        }, 201


class BookResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Single book',
                'examples': {
                    'application/json': {
                        'id': 1,
                        'title': '1984',
                        'author': 'George Orwell'
                    }
                }
            },
            404: {'description': 'Book not found'}
        }
    })
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'error': 'Book not found'}, 404

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author
        }, 200

    @swag_from({
        'responses': {
            200: {'description': 'Book deleted'},
            404: {'description': 'Book not found'}
        }
    })
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'error': 'Book not found'}, 404

        db.session.delete(book)
        db.session.commit()
        return {'status': 'success'}, 200
