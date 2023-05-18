from fastapi import FastAPI
from .schemas import *


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello maxe232m1"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.get("/process/")
async def say_hello(Data: MainInput):
    return {"message": f"Hello world!"}
