from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.database.database import engine, SessionLocal
from app.src.database import models
from fastapi.middleware.cors import CORSMiddleware

from app.src.pieces.district.service import parse_district
from app.src.pieces.industry.service import parse_industry
from app.src.pieces.patent.service import parse_patents
from app.src.pieces.user.router import router as auth_router
from app.src.pieces.calculation.router import router as calculation_router
from app.src.pieces.equipment.router import router as equipment_router
from app.src.pieces.currency.sheduled_update import schedule_currency_update


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://176.59.54.18",
    "http://176.59.54.18:80",
    "http://176.59.54.18:443",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(calculation_router)
app.include_router(equipment_router)


def fill_db(head_only: bool = False):
    only_first = 50 if head_only else None
    data = [
        (parse_district, 'srednyaa_kadastr_stoimost_po_okrugam.xlsx'),
        (parse_stanki, 'stanki_srednaya_csena.xlsx'),
        (parse_patents, 'patentirovanie_potencialniy_dohod_moskva.xlsx'),
        (parse_industry, 'obezlichenie_dannie.xlsm'),
    ]

    errors = 0
    for func, name in data:
        try:
            with SessionLocal() as db:
                func(name, db, only_first)
            print(f'SUCCESS: dataset {name} WAS downloaded')
        except Exception as e:
            print(f'ERROR: dataset {name} WAS NOT downloaded')
            print(e)
            errors += 1
        finally:
            print('-----------------------')
    if errors == 0:
        print('all datasets downloaded successfully')
    else:
        print(f'WARNING: some datasets WERE NOT downloaded successfully: {len(data) - errors}/{len(data)}')

    schedule_currency_update("RUB")



@app.on_event("startup")
async def startup_event():
    """
    Refresh table types by dropping all tables and creating them again
    Fill database with a few data from datasets
    """
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    fill_db(True)


from app.src.pieces.equipment.service import parse_stanki
@app.post("/parse")
async def parse(db: Session = Depends(get_db)):
    parse_patents('patentirovanie_potencialniy_dohod_moskva.xlsx', db)
