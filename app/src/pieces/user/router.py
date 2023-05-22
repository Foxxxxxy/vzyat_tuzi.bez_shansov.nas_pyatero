from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.src.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.src.database.common import get_db
from typing import Union
from datetime import datetime, timedelta
from jose import jwt
import re


from app.src.pieces.user.models import UserModel
from app.src.pieces.user.schemas import SignUpSchema, UserOutputSchema
from app.src.pieces.user import service as user_service
from app.src.security import auth_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> Union[UserOutputSchema, None]:
    user = user_service.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    user_return = UserOutputSchema.from_orm(user)
    return user_return


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/get_token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "level": user.level, "email": user.email}


password_pattern = r'[A-Za-z0-9@#$%^&+=]{8,}'


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/sign_up", response_model=UserOutputSchema)
async def sign_up(form: SignUpSchema, db: Session = Depends(get_db)):
    if not re.fullmatch(password_pattern, form.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    form.password = get_password_hash(form.password)
    user_service.check_user_level(form.level)
    if user_service.get_user_by_email(db, form.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="there is already a user with such email")
    result = user_service.create_user(db, form)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return result


@router.get("/{id}", response_model=UserOutputSchema)
async def get_user(id: int, db: Session = Depends(get_db), user: UserModel = Depends(auth_user)):
    result = user_service.get_user_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such user")
    return result


@router.get("/", response_model=list[UserOutputSchema])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = user_service.get_users(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such user")
    return result
