from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.pieces.currency.currency import Currency

router = APIRouter(
    prefix="/currency",
    tags=["currency"],
)

currency = Currency()


@router.get("/{currency_name}")
async def get_currency_by_name(currency_name: str, db: Session = Depends(get_db)) -> float:
    return currency.get_currency(currency_name, db)
