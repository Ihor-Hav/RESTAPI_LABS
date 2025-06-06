from fastapi import FastAPI
from app.routes import router as books_router


app = FastAPI()
app.include_router(books_router)
