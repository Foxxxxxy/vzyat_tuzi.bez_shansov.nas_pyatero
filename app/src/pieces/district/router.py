from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db

from app.src.pieces.district import service as district_service
from app.src.pieces.district.schemas import DistrictSchema, DistrictCreationSchema
from app.src.pieces.user.models import UserModel
from app.src.security import auth_user, auth_admin

router = APIRouter(
    prefix="/district",
    tags=["district"],
)


@router.get("/suggestions", response_model=list[DistrictSchema])
async def get_districts_suggestions(subtext: str = '', skip: int = 0, limit: int = 100,
                                    db: Session = Depends(get_db)):
    return district_service.get_district_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=DistrictSchema)
async def get_district(id: int, db: Session = Depends(get_db)):
    result = district_service.get_district_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No district with such id!")
    return result


@router.get("/", response_model=list[DistrictSchema])
async def get_districts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = district_service.get_districts(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No districts!")
    return result


@router.post("/", response_model=DistrictSchema)
async def add_district(schema: DistrictCreationSchema, db: Session = Depends(get_db),
                       user: UserModel = Depends(auth_admin)):
    return district_service.add_district(db, schema)


@router.put("/{id}", response_model=DistrictSchema)
async def update_district(id: int, schema: DistrictCreationSchema,
                          db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return district_service.update_district(db, id, schema)


@router.delete("/{id}", response_model=DistrictSchema)
async def delete_district(id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(auth_admin)):
    return district_service.delete_district(db, id)
