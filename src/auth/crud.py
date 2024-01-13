from fastapi import HTTPException, status
from fastapi_sqlalchemy import db

from src import models as auth_model
from src.auth import schemas
from src.utils import crypto_util

def create_user(user: schemas.UserCreate):
    db_user = auth_model.User(username=user.username, email=user.email, password=crypto_util.get_password_hash(user.password))
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    
    return db_user


def check_existing_user(username: str):
    existing_user = db.session.query(auth_model.User).filter(auth_model.User.username == username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    return existing_user


def find_token_by_id(token_id: int):
    token = db.session.query(auth_model.Token).filter(auth_model.Token.id == token_id).first()

    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    
    return token


def find_token_by_user_id(user_id: int):
    token = db.session.query(auth_model.Token).filter(auth_model.Token.user_id == user_id).first()

    if not token:
        return None
    
    return token


def update_token(token: schemas.Token):
    db.session.query(auth_model.Token).filter(auth_model.Token.id == token.id).update({"access_token": token.access_token, "refresh_token": token.refresh_token, "token_type": token.token_type, "status": token.status})
    db.session.commit()
    db.session.refresh(token)
    
    return token
