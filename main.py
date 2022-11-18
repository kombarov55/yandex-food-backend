from fastapi import FastAPI

import yandex_food_parser
from config import database

app = FastAPI()
database.base.metadata.create_all(bind=database.engine)
session = database.session_local()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/xlsx/{food_name}")
async def xlsx(food_name: str):
    yandex_food_parser.process_xlsx(session, food_name)
    return "OK"
