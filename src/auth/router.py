from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi_sqlalchemy import db

from src.auth import crud as auth_crud
from src.utils import jwt_util
from src.utils import constant_util

from src.auth import schemas as auth_schema
from src import models as auth_model


router = APIRouter(
    prefix="/api/v1",
    tags=["Auth"]
)


@router.post("/auth/signup", 
          response_model=auth_schema.User, 
          tags=["Auth"], 
          status_code=status.HTTP_201_CREATED,
          response_description="User created successfully")
async def create_user(user: auth_schema.UserCreate):
    auth_crud.check_existing_user(user.username)
    db_user = auth_crud.create_user(user)
    return db_user


@router.post("/auth/login", 
          response_model=auth_schema.Token, 
          tags=["Auth"],
          status_code=status.HTTP_201_CREATED,
          response_description="Token created successfully")
async def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_util.authenticate_user(from_data.username, from_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=constant_util.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=constant_util.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_util.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = jwt_util.create_access_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token,"refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/auth/token/refresh",
            response_model=auth_schema.Token,
            tags=["Auth"],
            status_code=status.HTTP_201_CREATED,
            response_description="Token refreshed successfully")
async def refresh_token(refresh_token: auth_schema.RefreshToken):
    token = await jwt_util.refresh_token(refresh_token.refresh_token)
    return token
