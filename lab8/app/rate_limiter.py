from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request, FastAPI
from app.auth import get_current_user
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

def custom_key_func(request: Request):
    return request.state.user or get_remote_address(request)


limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")



async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )


class CustomRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            user = await get_current_user(request)
            request.state.user = user.get("username")
        except:
            request.state.user = None
        response = await call_next(request)
        return response



def init_rate_limiter(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
