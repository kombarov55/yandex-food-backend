from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from model.food import FoodVO


def save(session: Session, vo: FoodVO):
    session.add(vo)
    session.commit()


def save_all(session: Session, xs: list):
    for x in xs:
        if not session.query(exists().where(FoodVO.id == x.id)).scalar():
            session.add(x)
    session.commit()


def get_all(session: Session, xlsx_request_id: int):
    return session.query(FoodVO).filter(FoodVO.xlsx_request_id == xlsx_request_id).all()


def delete_by_xlsx_request_id(session: Session, xlsx_request_id: int):
    session.query(FoodVO).filter(FoodVO.xlsx_request_id == xlsx_request_id).delete()
    session.commit()
