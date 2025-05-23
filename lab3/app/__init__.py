from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .config import Config


load_dotenv(override=True)


db = SQLAlchemy()


def create_app():
    api = Flask(__name__)

    api.config.from_object(Config)

    db.init_app(api)

    with api.app_context():
        from . import views
        db.create_all()
    
    from .views import books_bp
    api.register_blueprint(books_bp)

    return api

api = create_app()