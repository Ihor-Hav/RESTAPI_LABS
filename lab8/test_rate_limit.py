import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from main import app
import os

client = TestClient(app)


FAKE_USER = {"username": "testuser", "email": "test@example.com"}

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer " + os.getenv("TOKEN")}


@pytest.fixture(autouse=True)
def mock_get_current_user():
    with patch("app.auth.get_current_user", new=AsyncMock(return_value=FAKE_USER)):
        yield

@pytest.fixture(autouse=True)
def mock_books_collection():
    fake_books = [
        {"_id": "1", "title": "Book One"},
        {"_id": "2", "title": "Book Two"},
    ]
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = fake_books

    with patch("app.routes.books_collection") as mock_collection:
        mock_collection.find.return_value.sort.return_value.limit.return_value = mock_cursor
        mock_collection.find_one.return_value = fake_books[0]
        mock_collection.insert_one.return_value.inserted_id = "1"
        mock_collection.delete_one.return_value.deleted_count = 1
        yield mock_collection

@pytest.mark.asyncio
async def test_authorized_user_within_limit(auth_headers):
    response = client.get("/books", headers=auth_headers)
    assert response.status_code == 200
    assert "books" in response.json()

@pytest.mark.asyncio
async def test_authorized_user_exceeds_limit(auth_headers):
    for _ in range(10):
        response = client.get("/books", headers=auth_headers)
        assert response.status_code == 200
    # 11-й запит перевищить ліміт
    response = client.get("/books", headers=auth_headers)
    assert response.status_code == 429  # Too Many Requests

@pytest.mark.asyncio
async def test_anonymous_user_within_limit():
    response = client.get("/public-books")
    assert response.status_code == 200
    assert "books" in response.json()

@pytest.mark.asyncio
async def test_anonymous_user_exceeds_limit():
    for _ in range(2):
        response = client.get("/public-books")
        assert response.status_code == 200
    # 3-й запит — перевищення
    response = client.get("/public-books")
    assert response.status_code == 429  # Too Many Requests
