from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

import yandex_food_parser
from config import database
from repository import xlsx_request_repository

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
    vo = xlsx_request_repository.create(session, food_name)
    return "OK {}".format(vo.id)


@app.get("/xlsx_requests")
async def get_all_xlsx_requests():
    return xlsx_request_repository.get_all(session)


app.mount("/static", StaticFiles(directory="reports"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
