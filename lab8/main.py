from fastapi import FastAPI
from app.routes import router as books_router
from app.auth_routes import router as auth_router
from app.rate_limiter import init_rate_limiter, CustomRateLimitMiddleware
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()


app.add_middleware(SlowAPIMiddleware)
app.add_middleware(CustomRateLimitMiddleware)


init_rate_limiter(app)


app.include_router(auth_router)
app.include_router(books_router)
