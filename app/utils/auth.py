from fastapi import Depends, HTTPException
from typing import Annotated
from ..models.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from ..core.config import SECRET_KEY, ALGORITHM


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_date: timedelta):
    encode = {
        'sub': username,
        'id': user_id
    }
    expires = datetime.now(timezone.utc) + expires_date
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None and user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate user.")
        return {'username': username, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate user.")

user_dependency = Annotated[dict, Depends(get_current_user)]
