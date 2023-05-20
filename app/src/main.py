from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.src.database.common import get_db
from app.src.database.database import engine
from app.src.database import models
from fastapi.middleware.cors import CORSMiddleware

from app.src.pieces.user.router import router as auth_router
from app.src.pieces.calculation.router import router as calculation_router

# todo change for alembic
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
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


from app.src.pieces.equipment.service import parse_stanki
@app.post("/parse")
async def get_access_token(db: Session = Depends(get_db)):
    parse_stanki('stanki_srednaya_csena.xlsx', db)
    #user = authenticate_user(form_data.username, form_data.password, db)