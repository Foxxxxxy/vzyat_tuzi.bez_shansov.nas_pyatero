from fastapi import FastAPI

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
