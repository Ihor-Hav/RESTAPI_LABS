books = [
    {
        "id": 0,
        "author": "J.K. Rowling",
        "title": "Harry Potter and the Sorcerer's Stone"
    }
]

def generate_new_id():
    return max((book["id"] for book in books), default=-1) + 1
