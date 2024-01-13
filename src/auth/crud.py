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
