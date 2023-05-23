# todo - когда будем делать пополнение справочников
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db


from app.src.pieces.building.schemas import BuildingSchema
from app.src.pieces.building import service as building_service

router = APIRouter(
    prefix="/building",
    tags=["building"],
)


@router.get("/suggestions", response_model=list[BuildingSchema])
async def get_buildings_suggestions(subtext: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return building_service.get_building_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=BuildingSchema)
async def get_building(id: int, db: Session = Depends(get_db)):
    result = building_service.get_building_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such building")
    return result


@router.get("/", response_model=list[BuildingSchema])
async def get_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = building_service.get_buildings(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such building")
    return result

