from enum import Enum

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.src.pieces.user.models import UserModel
from app.src.pieces.user.schemas import SignUpSchema, EUserLevel


def get_user_by_id(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserModel]:
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, sign_up_form: SignUpSchema) -> UserModel:
    data = sign_up_form.dict()
    data['hashed_password'] = data['password']
    del data['password']
    db_user = UserModel(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_user_level(level):
    if level < EUserLevel.user or level > EUserLevel.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="no such user level")
    return level