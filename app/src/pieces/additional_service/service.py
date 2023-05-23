from app.src.pieces.additional_service.models import AdditionalServiceModel
from app.src.pieces.additional_service.schemas import AdditionalServiceCreationSchema
from sqlalchemy.orm import Session


def get_additional_service_by_id(db: Session, additional_service_id: int) -> AdditionalServiceModel:
    return db.query(AdditionalServiceModel) \
        .filter(AdditionalServiceModel.id == additional_service_id).first()


def get_additional_services(db: Session, skip: int = 0, limit: int = 100) -> list[AdditionalServiceModel]:
    return db.query(AdditionalServiceModel).offset(skip).limit(limit).all()


def get_additional_service_suggestions(db: Session, subtext: str = '',
                                       skip: int = 0, limit: int = 100) -> list[AdditionalServiceModel]:
    if subtext == '':
        return get_additional_services(db, skip, limit)
    return db.query(AdditionalServiceModel) \
        .filter(AdditionalServiceModel.name.contains(subtext)).offset(skip).limit(limit).all()


def add_additional_service(db: Session,
                           additional_service: AdditionalServiceCreationSchema) -> AdditionalServiceModel:
    additional_service = AdditionalServiceModel(**additional_service.dict())
    db.add(additional_service)
    db.commit()
    db.refresh(additional_service)
    return additional_service


def delete_additional_service(db: Session, id: int,) -> AdditionalServiceModel:
    additional_service = db.query(AdditionalServiceModel) \
        .filter(AdditionalServiceModel.id == id).first()
    db.delete(additional_service)
    db.commit()
    return additional_service
