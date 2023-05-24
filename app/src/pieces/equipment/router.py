from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.database.common import get_db

from app.src.pieces.equipment.schemas import EquipmentSchema, EquipmentCreationSchema
from app.src.pieces.equipment import service as equipment_service
from app.src.pieces.user.models import UserModel
from app.src.security import auth_user, auth_admin

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No equipment with such id!")
    return result


@router.get("/", response_model=list[EquipmentSchema])
async def get_equipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = equipment_service.get_equipments(db, skip, limit)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No equipment!")
    return result


@router.post("/", response_model=EquipmentSchema)
async def add_equipment(schema: EquipmentCreationSchema, db: Session = Depends(get_db),
                        user: UserModel = Depends(auth_admin)):
    return equipment_service.add_equipment(db, schema)


@router.put("/{id}", response_model=EquipmentSchema)
async def update_equipment(id: int, schema: EquipmentCreationSchema,
                           db: Session = Depends(get_db), user: UserModel = Depends(auth_admin)):
    return equipment_service.update_equipment(db, id, schema)


@router.delete("/{id}", response_model=EquipmentSchema)
async def delete_additional_service(id: int, db: Session = Depends(get_db),
                                    user: UserModel = Depends(auth_admin)):
    return equipment_service.delete_equipment(db, id)
