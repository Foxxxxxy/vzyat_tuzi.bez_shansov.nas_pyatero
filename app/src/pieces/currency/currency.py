from fastapi import Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.currency.models import CurrencyModel


class Currency:

    @staticmethod
    def get_currency(name: str, db: Session = Depends(get_db)):
        currency = db.query(CurrencyModel).filter(CurrencyModel.name == name).first()
        return currency.value
