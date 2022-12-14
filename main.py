import sys

import uvicorn
from fastapi import FastAPI, Response, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from config import database
from repository import xlsx_request_repository, account_repository, compilation_repository
from service import restore_pwd_service, search_food_service, prepare_data_service, compilation_service

app = FastAPI()
database.base.metadata.create_all(bind=database.engine)

def get_session():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/xlsx/{food_name}")
async def xlsx(food_name: str, session: Session = Depends(get_session)):
    vo = xlsx_request_repository.create(session, food_name)
    return "OK {}".format(vo.id)


@app.get("/xlsx_requests")
async def get_all_xlsx_requests(response: Response):
    response.headers["x-cat-foo"] = "hello worldbash"
    response.headers["allow-origins"] = "*"
    response.headers["allow-credentials"] = "true"
    response.headers["allow-methods"] = "*"
    response.headers["allow-headers"] = "*"
    return xlsx_request_repository.get_all(database.session_local())

@app.post("/account")
async def register(body: dict, session: Session = Depends(get_session)):
    return account_repository.register(session, body)


@app.post("/account/login")
async def login(body: dict, session: Session = Depends(get_session)):
    result = account_repository.login(session, body)
    return result


@app.get("/account/restore_pwd/{email}")
async def restore_pwd(email: str, session: Session = Depends(get_session)):
    restore_pwd_service.run(session, email)


@app.get("/search_food/{food_name}/{amount}/{email}")
async def search_food(food_name: str, amount: int, email:str, session: Session = Depends(get_session)):
    return search_food_service.find(food_name, email)


@app.post("/account/{email}/compilation/{food_id}")
async def add_compilation_item(email: str, food_id: int, session: Session = Depends(get_session)):
    compilation_repository.add_item(session, email, food_id)
    return "OK"

@app.post("/account/{email}/compilation/{name}/{food_id}/{prev_name}")
async def move_compilation_item(email: str, name: str, prev_name: str, food_id: int, session: Session = Depends(get_session)):
    compilation_repository.add_item(session, email, food_id, name)
    compilation_repository.remove_item(session, email, prev_name, food_id)
    return "OK"


@app.delete("/account/{email}/compilation/{name}/{food_id}")
async def remove_compilation_item(email: str, name: str, food_id: int, session: Session = Depends(get_session)):
    compilation_repository.remove_item(session, email, name, food_id)
    return "OK"


@app.delete("/account/{email}/compilation/{name}")
async def remove_compilation(email: str, name: str, session: Session = Depends(get_session)):
    compilation_repository.remove_compilation(session, email, name)
    return "OK"


@app.get("/account/{email}/compilation")
async def find_all_compilations(email: str, session: Session = Depends(get_session)):
    compilation_repository.fix(session)
    return compilation_service.find(session, email)


@app.get("/fix")
async def fix(session: Session = Depends(get_session)):
    compilation_repository.fix(session)


app.mount("/static", StaticFiles(directory="reports"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_prod():
    print(sys.argv)
    if len(sys.argv) < 2:
        return False
    if sys.argv[1] == "prod":
        return True
    return False


if __name__ == "__main__":
    prepare_data_service.run_background()

    if is_prod():
        print("######################")
        print("starting in prod mode")
        print("######################")
        uvicorn.run(
            app, port=8000, host='0.0.0.0',
            ssl_keyfile="/etc/letsencrypt/live/novemis.ru/privkey.pem",
            ssl_certfile="/etc/letsencrypt/live/novemis.ru/fullchain.pem")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
