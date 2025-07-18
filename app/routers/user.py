from fastapi import APIRouter, HTTPException
from starlette import status
from ..models.models import User
from ..core.database import db_dependency
from ..shemas.shemas import UserRequest, UserVerification
from ..utils.auth import user_dependency, bcrypt_context


router = APIRouter(
    prefix="/me",
    tags=["me"]
)


@router.get("/full-profile", status_code=status.HTTP_200_OK)
async def get_profile(user: user_dependency, db: db_dependency):
    user_model = db.query(User).filter(User.id == user.get("user_id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="This user does not Exists")
    return user_model


@router.put("/update-profile", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(user: user_dependency, db: db_dependency, user_request: UserRequest):
    user_model = db.query(User).filter(User.id == user.get('user_id')).first()
    if user is None:
        raise HTTPException(status_code=404, detail="This user does not Exists")
    user_model.email = user_request.email
    user_model.username = user_request.username

    db.add(user_model)
    db.commit()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticate Failed")
    user_model = db.query(User).filter(User.username == user.get('username')).first()
    if bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
