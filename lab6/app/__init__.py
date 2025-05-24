from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger
from dotenv import load_dotenv
from .config import Config

load_dotenv(override=True)

db = SQLAlchemy()
swagger = Swagger()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    swagger.init_app(app)

    api = Api(app)

    with app.app_context():
        from .models import Book
        db.create_all()

    from .resources import BookListResource, BookResource
    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')

    return app

api = create_app()
