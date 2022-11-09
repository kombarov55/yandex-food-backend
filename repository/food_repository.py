from sqlalchemy.orm import Session

from model.food import FoodVO


def save(session: Session, vo: FoodVO):
    session.add(vo)
    session.commit()
