from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.database.database import engine, SessionLocal
from app.src.database import models
from fastapi.middleware.cors import CORSMiddleware

from app.src.pieces.building.service import parse_buildings
from app.src.pieces.district.service import parse_district
from app.src.pieces.industry.service import parse_industry
from app.src.pieces.patent.service import parse_patents


from app.src.pieces.user.router import router as auth_router, get_password_hash
from app.src.pieces.calculation.router import router as calculation_router
from app.src.pieces.equipment.router import router as equipment_router
from app.src.pieces.building.router import router as building_router
from app.src.pieces.industry.router import router as industry_router
from app.src.pieces.additional_service.router import router as additional_service_router
from app.src.pieces.currency.router import router as currency_router
from app.src.pieces.district.router import router as district_router

from app.src.pieces.currency.sheduled_update import schedule_currency_update

from app.src.pieces.user.schemas import SignUpSchema, EUserLevel
from app.src.pieces.user.service import create_user

prefixes = ['http://', '', 'https://']
bodies = ['localhost', 'smetaverse.ru', 'www.smetaverse.ru', '176.59.54.18']
ports = [':80', ':443', ':3000', ':3030', ':8000', ':8080', '']

origins = []

for prefix in prefixes:
    for body in bodies:
        for port in ports:
            origins.append(prefix + body + port)

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
app.include_router(building_router)
app.include_router(industry_router)
app.include_router(additional_service_router)
app.include_router(currency_router)
app.include_router(district_router)


level_to_name = {
    EUserLevel.user: 'user',
    EUserLevel.moderator: 'moderator',
    EUserLevel.admin: 'admin',
}


def create_template_user_schema(level: EUserLevel):
    name = level_to_name[level]
    return SignUpSchema(password=get_password_hash('12345678'),
                          email=name,
                          name=name,
                          last_name=name,
                          organisation_name=name,
                          inn='123321',
                          web_site='https://site.ru',
                          level=level)


def fill_db(head_only: bool = False):
    with SessionLocal() as db:
        create_user(db, create_template_user_schema(EUserLevel.user))
        create_user(db, create_template_user_schema(EUserLevel.admin))
        print('users created')
    only_first = 50 if head_only else None
    data = [
        (parse_district, 'srednyaa_kadastr_stoimost_po_okrugam.xlsx'),
        (parse_stanki, 'stanki_srednaya_csena.xlsx'),
        (parse_patents, 'patentirovanie_potencialniy_dohod_moskva.xlsx'),
        (parse_industry, 'obezlichenie_dannie.xlsm'),
        (parse_buildings, 'building_dataset.xlsx'),
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

    # scheduled currency update for dollar course
    schedule_currency_update("RUB")



@app.on_event("startup")
async def startup_event():
    """
    Refresh table types by dropping all tables and creating them again
    Fill database with a few data from datasets
    Add base users
    """
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    fill_db(True)


from app.src.pieces.equipment.service import parse_stanki
@app.post("/parse")
async def parse(db: Session = Depends(get_db)):
    parse_patents('patentirovanie_potencialniy_dohod_moskva.xlsx', db)
