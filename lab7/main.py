from fastapi import FastAPI
from app.routes import router as books_router
from app.auth_routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(books_router)
