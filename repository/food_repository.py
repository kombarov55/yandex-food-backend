from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import exists

from config import database, app_config
from model.food import FoodVO
from model.search_food import FoodChartDto
from repository import restaurant_repository
from service import search_food_service


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


def search_lowest_price_food(session: Session, food_name: str, xlsx_request_id: int, amount: int):
    return session.query(FoodVO)\
        .filter(FoodVO.xlsx_request_id == xlsx_request_id) \
        .filter(func.lower(FoodVO.name).contains(food_name.lower()))\
        .order_by(FoodVO.price.asc())\
        .limit(amount)\
        .all()

def search_highest_price_food(session: Session, food_name: str, xlsx_request_id: int, amount: int):
    return session.query(FoodVO)\
        .filter(FoodVO.xlsx_request_id == xlsx_request_id) \
        .filter(func.lower(FoodVO.name).contains(food_name.lower()))\
        .order_by(FoodVO.price.desc())\
        .limit(amount)\
        .all()


def search_biggest_weight_food(session: Session, food_name: str, xlsx_request_id: int, amount: int):
    return session.query(FoodVO)\
        .filter(FoodVO.xlsx_request_id == xlsx_request_id) \
        .filter(func.lower(FoodVO.name).contains(food_name.lower())) \
        .filter(FoodVO.weight is not None)\
        .order_by(FoodVO.weight.desc())\
        .limit(amount)\
        .all()


def search_avg_price(session: Session, food_name: str, xlsx_request_id: int):
    return session.query(FoodVO)\
        .with_entities(func.avg(FoodVO.price).label("average"))\
        .filter(FoodVO.xlsx_request_id == xlsx_request_id) \
        .filter(func.lower(FoodVO.name).contains(food_name.lower()))\
        .all()[0]["average"]


def get_chart_data(session: Session, food_name: str, xlsx_request_id: int):
    stmt = session.query(FoodVO).filter(FoodVO.xlsx_request_id == xlsx_request_id).filter(
        or_(func.lower(FoodVO.name).contains(func.lower(food_name)), func.lower(FoodVO.name).startswith(func.lower(food_name))))
    print(stmt)
    food_list = stmt \
        .all()

    restaurants = restaurant_repository.find_all(session, xlsx_request_id)

    result = []

    for x in food_list:
        result.append(FoodChartDto(
            shop_name=find_restaurant(restaurants, x.restaurant_id).name,
            price=x.price
        ))

    return result


def find_restaurant(xs, restaurant_id):
    for x in xs:
        if x.slug == restaurant_id:
            return x
    return None


if __name__ == "__main__":
    DATABASE_URL = "sqlite:///{}".format("../yandex-food.db")

    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    result = get_chart_data(session, "Цезарь", 1)

    print(result)
