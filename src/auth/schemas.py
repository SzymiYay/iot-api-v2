from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    username: str = None

class TokenInDB(BaseModel):
    id: int
    refresh_token: str
    status: bool
    expires: datetime
    time_created: datetime
    time_updated: datetime
    user_id: int



class User(BaseModel):
    username: str
    email: str or None = None

    class Config:
        orm_mode = True

class UserCreate(User):
    password: str

class UserInDB(UserCreate):
    id: int
    disabled: bool or None = False
    time_created: datetime
    time_updated: datetime

    class Config:
        orm_mode = True