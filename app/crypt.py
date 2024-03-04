import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional
import json
from jwt import decodeJWT,encodeJWT
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"




def verify_hash(password,savedSalt):
    savedSalt = savedSalt.encode('utf-8')
    savedSalt = base64.b64decode(savedSalt)
    key = hashlib.pbkdf2_hmac(
    'sha256',
    password.encode('utf-8'), 
    savedSalt, 
    100000
    )   
    key = base64.b64encode(key)
    return key


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = encodeJWT(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_email(token):
    decoded = decodeJWT(token, SECRET_KEY)
    user_email = json.loads(decoded["payload"])["sub"]
    return user_email