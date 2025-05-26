from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import Token, LoginRequest
from .auth import authenticate_user, create_access_token, create_refresh_token, verify_token, REFRESH_SECRET_KEY

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token({"sub": user["username"]})
    refresh_token = create_refresh_token({"sub": user["username"]})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    user = verify_token(refresh_token, secret=REFRESH_SECRET_KEY)
    access_token = create_access_token({"sub": user["username"]})
    new_refresh_token = create_refresh_token({"sub": user["username"]})
    return {"access_token": access_token, "refresh_token": new_refresh_token}
