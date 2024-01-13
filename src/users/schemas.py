from pydantic import BaseModel
from datetime import datetime

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

class Device(BaseModel):
    name: str

class DeviceReturn(Device):
    id: int
    name: str
    user_id: int

class DeviceInDB(Device):
    id: int
    time_created: datetime
    time_updated: datetime
    user_id: int

    class Config:
        orm_mode = True