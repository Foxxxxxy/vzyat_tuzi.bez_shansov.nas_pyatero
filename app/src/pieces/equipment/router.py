# todo - когда будем делать пополнение справочников
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db


from app.src.pieces.equipment.schemas import EquipmentSchema
from app.src.pieces.equipment import service as equipment_service


router = APIRouter(
    prefix="/equipment",
    tags=["equipment"],
)


@router.get("/suggestions", response_model=list[EquipmentSchema])
async def get_equipments_suggestions(subtext: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return equipment_service.get_equipment_suggestions(db, subtext, skip, limit)


@router.get("/{id}", response_model=EquipmentSchema)
async def get_equipment(id: int, db: Session = Depends(get_db)):
    result = equipment_service.get_equipment_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such user")
    return result


@router.get("/", response_model=list[EquipmentSchema])
async def get_equipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = equipment_service.get_equipments(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such user")
    return result

