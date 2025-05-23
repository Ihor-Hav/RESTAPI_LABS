from . import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(225), nullable=False)
    author = db.Column(db.String(225), nullable=False)
    
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'


