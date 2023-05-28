from sqlalchemy.orm import Session

from app.src.pieces.currency.models import CurrencyModel


class Currency:

    @staticmethod
    def get_currency(name: str, db: Session):
        currency = db.query(CurrencyModel).filter(CurrencyModel.name == name).first()
        return currency.value
