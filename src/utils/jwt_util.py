from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi_sqlalchemy import db
from fastapi.security import OAuth2PasswordBearer

from src.utils import crypto_util
from src.utils import constant_util

from src.users import schemas as user_schema
from src.auth import schemas as auth_schema

from src import models

from src import db_config

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
    )

# async def get_user(username: str) -> user_schema.UserInDB or None:
#     query = db_config.users.select().where(db_config.users.c.username == username)
#     db_user = await db_config.database.fetch_one(query)
#     if db_user:
#         return db_user
#     return None


def get_user(username: str) -> user_schema.UserInDB or None:
    db_user = db.session.query(models.User).filter(models.User.username == username).first()
    if db_user:
        return db_user
    return None

    
def authenticate_user(username: str, password: str) -> user_schema.UserInDB or None:
    user = get_user(username)
    if not user:
        return False
    if not crypto_util.verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=constant_util.SECRET_KEY, algorithm=constant_util.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> user_schema.UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, key=constant_util.SECRET_KEY, algorithms=[constant_util.ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = auth_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)) -> user_schema.User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    return current_user


async def refresh_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(refresh_token, key=constant_util.SECRET_KEY, algorithms=[constant_util.ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = auth_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=constant_util.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=constant_util.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_access_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token,"refresh_token": refresh_token, "token_type": "bearer"}
