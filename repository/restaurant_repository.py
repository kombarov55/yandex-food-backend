from sqlalchemy.orm import Session

from model.restaurant import RestaurantVO


def save(session: Session, restaurant: RestaurantVO):
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


def find_all(session: Session, xlsx_request_id: int):
    return session.query(RestaurantVO).filter(RestaurantVO.xlsx_request_id == xlsx_request_id).all()


def delete_by_xlsx_request_id(session: Session, xlsx_request_id: int):
    session.query(RestaurantVO).filter(RestaurantVO.xlsx_request_id == xlsx_request_id).delete()
    session.commit()
