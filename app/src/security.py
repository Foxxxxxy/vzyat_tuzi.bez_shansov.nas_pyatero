from app.src.pieces.user.models import UserModel
from app.src.pieces.user.schemas import EUserLevel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.src.config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from app.src.pieces.user.service import get_user_by_email
from sqlalchemy.orm import Session
from app.src.database.common import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/get_token")

prod_mode = True


async def get_user_secured(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, username)
    if user is None:
        raise credentials_exception
    return user


async def _check_for_permission(user: UserModel, level: EUserLevel, name: str) -> UserModel:
    if prod_mode and user.role < level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You need to be at least {name}"
        )
    return user


async def auth_user(user: UserModel = Depends(get_user_secured)) -> UserModel:
    return await _check_for_permission(user, EUserLevel.user, 'user')


async def auth_moderator(user: UserModel = Depends(get_user_secured)) -> UserModel:
    return await _check_for_permission(user, EUserLevel.moderator, 'moderator')


async def auth_admin(user: UserModel = Depends(get_user_secured)) -> UserModel:
    return await _check_for_permission(user, EUserLevel.admin, 'admin')
