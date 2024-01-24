from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta or None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key="b8cc9b918728fb4c7f67ba6bc321d281b8b117c24d83863815134afe8fa496fb", algorithm="HS256")
    return encoded_jwt

print(create_access_token({"sub": "admin"}, 1000000))

