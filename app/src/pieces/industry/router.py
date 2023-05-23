# todo - когда будем делать пополнение справочников
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db


from app.src.pieces.industry.schemas import IndustrySchema
from app.src.pieces.industry import service as industry_service
from app.src.pieces.user.models import UserModel
from app.src.security import auth_user

router = APIRouter(
    prefix="/industry",
    tags=["industry"],
)


@router.get("/suggestions", response_model=list[IndustrySchema])
async def get_industries_suggestions(subtext: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return industry_service.get_industry_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=IndustrySchema)
async def get_industry(id: int, db: Session = Depends(get_db)):
    result = industry_service.get_industry_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such industry")
    return result


@router.get("/", response_model=list[IndustrySchema])
async def get_industries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = industry_service.get_industries(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such industry")
    return result

