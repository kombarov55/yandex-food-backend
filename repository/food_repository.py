from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import exists

from config import database
from model.food import FoodVO, PlaceType
from model.restaurant import RestaurantVO
from model.search_food import FoodChartDto, FoodDto
from repository import restaurant_repository


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


def search_lowest_price_food(session: Session, food_name: str, restaurant_list: list, amount: int):
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id, category_id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") " \
              "and price is not null " \
              "order by price asc " \
              "limit :limit"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), limit=amount)

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6]
            ))

        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def search_highest_price_food(session: Session, food_name: str, restaurant_list: list, amount: int):
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id, category_id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") " \
              "and price is not null " \
              "order by price desc " \
              "limit :limit"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), limit=amount)

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6]
            ))

        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def search_biggest_weight_food(session: Session, food_name: str, restaurant_list: list, amount: int):
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id, category_id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") " \
              "and weight is not null " \
              "order by weight desc " \
              "limit :limit"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), limit=amount)

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6]
            ))

        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def search_avg_price(session: Session, food_name: str, xlsx_request_id: int):
    return session.query(FoodVO) \
        .with_entities(func.avg(FoodVO.price).label("average")) \
        .filter(FoodVO.xlsx_request_id == xlsx_request_id) \
        .filter(func.lower(FoodVO.name).contains(food_name.lower())) \
        .all()[0]["average"]


def get_chart_data(food_name: str, restaurants: list):
    with database.engine.connect() as con:
        sql = "select name, price, restaurant_id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") "
        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower())

        result = []

        for row in rows:
            name = row[0]
            price = row[1]
            slug = row[2]
            restaurant_name = find_restaurant(restaurants, slug).name

            result.append(FoodChartDto(
                shop_name="{} ({})".format(name, restaurant_name),
                price=price
            ))
        return result


def find_best_food(restaurant_list: list, food_name: str, amount: int):
    with open("./best-food.sql", "r") as file:
        sql = file.read().rstrip()
    with database.engine.connect() as con:
        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), amount=amount)
        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6]
            ))
        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def convert_to_dto(vo, restaurant_list):
    restaurant = find_restaurant(restaurant_list, vo.restaurant_id)
    return FoodDto(
        name=vo.name,
        src=vo.src.replace("{w}", "400").replace("{h}", "400"),
        price=vo.price,
        restaurant_name=restaurant.name,
        address=restaurant.address,
        weight=vo.weight,
        rating=restaurant.rating,
        link=build_link(vo, restaurant))


def find_restaurant(xs, restaurant_id):
    for x in xs:
        if x.slug == restaurant_id:
            return x
    return None


def build_link(vo: FoodVO, restaurant: RestaurantVO):
    if restaurant.place_type == PlaceType.restaurant:
        return "https://eda.yandex.ru/moscow/r/{}?category={}&item={}&placeSlug={}".format(restaurant.slug, vo.category_id, vo.external_id, restaurant.slug)
    else:
        return "https://eda.yandex.ru/retail/{}/product/{}?placeSlug={}".format(vo.restaurant_id, vo.external_id,
                                                                                vo.restaurant_id)
