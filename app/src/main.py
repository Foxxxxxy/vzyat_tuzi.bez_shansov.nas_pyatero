from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.database.database import engine
from app.src.database import models
from fastapi.middleware.cors import CORSMiddleware

from app.src.pieces.district.service import parse_district
from app.src.pieces.patent.service import parse_patents
from app.src.pieces.user.router import router as auth_router
from app.src.pieces.calculation.router import router as calculation_router
from app.src.pieces.equipment.router import router as equipment_router

# todo change for alembic
models.Base.metadata.create_all(bind=engine)

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


from app.src.pieces.equipment.service import parse_stanki
@app.post("/parse")
async def parse(db: Session = Depends(get_db)):
    parse_patents('patentirovanie_potencialniy_dohod_moskva.xlsx', db)
