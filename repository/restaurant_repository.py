from sqlalchemy.orm import Session

from model.restaurant import RestaurantVO


def save(session: Session, restaurant: RestaurantVO):
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


def find_all(session: Session):
    return session.query(RestaurantVO).all()
