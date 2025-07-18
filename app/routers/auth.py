from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import Annotated
from ..models.models import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from ..core.database import db_dependency
from ..shemas.shemas import CreateUserRequest, Token
from ..utils.auth import user_dependency, bcrypt_context, create_access_token, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.post("/register", response_model=Token)
async def register(db: db_dependency, user_request: CreateUserRequest):
    user = db.query(User).filter(User.email == user_request.email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email already registered')
    create_user_model = User(
        email=user_request.email,
        username= user_request.username,
        hashed_password=bcrypt_context.hash(user_request.password)
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    token = create_access_token(create_user_model.username, create_user_model.id, timedelta(minutes=20))
    return {"access_token": token}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(form_data.username, user.id, timedelta(minutes=20))
    return {"access_token": token}


@router.get("/profile")
async def my_profile(user: user_dependency):
    return {"user_id": user.get("user_id"), "username": user.get("username")}
