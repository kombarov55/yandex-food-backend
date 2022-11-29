import uvicorn
from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

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
async def get_all_xlsx_requests(response: Response):
    response.headers["x-cat-foo"] = "hello worldbash"
    response.headers["allow-origins"] = "*"
    response.headers["allow-credentials"] = "true"
    response.headers["allow-methods"] = "*"
    response.headers["allow-headers"] = "*"
    return xlsx_request_repository.get_all(session)


app.mount("/static", StaticFiles(directory="reports"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
