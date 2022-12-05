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


def count(food_name: str):
    with database.engine.connect() as con:
        return con.execute("select count(*) "
                    "from food "
                    "where name like :name || '%' " 
                    "or name like '%' || :name || '%' " 
                    "or name like :lower_name || '%' " 
                    "or name like '%' || :lower_name || '%'", name=food_name.capitalize(), lower_name=food_name.lower())\
            .scalar()


def search_lowest_price_food(session: Session, food_name: str, restaurant_list: list, amount: int, place_type: str):
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id, category_id, id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and place_type = :place_type " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") " \
              "and price is not null " \
              "order by price asc " \
              "limit :limit"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), limit=amount,
                           place_type=place_type)

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6],
                id = row[7]
            ))

        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def search_highest_price_food(session: Session, food_name: str, restaurant_list: list, amount: int, place_type):
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id, category_id, id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and place_type = :place_type " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") " \
              "and price is not null " \
              "order by price desc " \
              "limit :limit"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), limit=amount,
                           place_type=place_type)

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6],
                id=row[7]
            ))

        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def search_biggest_weight_food(session: Session, food_name: str, restaurant_list: list, amount: int, place_type: str):
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id, category_id, id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and place_type = :place_type " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") " \
              "and weight is not null " \
              "order by weight desc " \
              "limit :limit"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower(), limit=amount,
                           place_type=place_type)

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6],
                id=row[7]
            ))

        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def search_avg_price(food_name: str, place_type: str):
    with database.engine.connect() as con:
        result = con.execute("select avg(price) "
                             "from food "
                             "where xlsx_request_id = 1 "
                             "and place_type = :place_type "
                             "and ("
                             "name like :food_name || '%' "
                             "or name like '%' || :food_name || '%' "
                             "or name like :food_name_lower || '%' "
                             "or name like '%' || :food_name_lower || '%')",
                             place_type=place_type,
                             food_name=food_name.capitalize(),
                             food_name_lower=food_name.lower())
        return result.scalar()


def get_chart_data(food_name: str, restaurants: list, place_type: str):
    with database.engine.connect() as con:
        sql = "select name, price, restaurant_id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and place_type = :place_type " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") "
        rows = con.execute(sql, place_type=place_type, name=food_name.capitalize(), lower_name=food_name.lower())

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


def find_best_food(restaurant_list: list, food_name: str, amount: int, place_type: str):
    with open("./best-food.sql", "r") as file:
        sql = file.read().rstrip()
    with database.engine.connect() as con:
        rows = con.execute(sql,
                           name=food_name.capitalize(),
                           lower_name=food_name.lower(),
                           amount=amount,
                           place_type=place_type)
        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5],
                category_id=row[6],
                id=row[7]
            ))
        return list(map(lambda x: convert_to_dto(x, restaurant_list), food_list))


def convert_to_dto(vo, restaurant_list):
    restaurant = find_restaurant(restaurant_list, vo.restaurant_id)
    return FoodDto(
        id=vo.id,
        name=vo.name,
        src=vo.src.replace("{w}", "400").replace("{h}", "400"),
        price=vo.price,
        restaurant_name=restaurant.name,
        address=restaurant.address,
        weight=vo.weight,
        rating=restaurant.rating,
        link=build_link(vo, restaurant))


def find_by_ids(ids_joined: list):
    with database.engine.connect() as con:
        sql = """
        select  food.id, 
        food.name, 
        food.src, 
        price, 
        r.name restaurant_name,
        r.address address,
        weight,
        r.rating restaurant_rating, 
        external_id, 
        category_id, 
        r.place_type,
        r.slug
        from food 
        join restaurant r on food.restaurant_id = r.slug 
        where food.xlsx_request_id = 1
        and food.id in ({})
        """.format(ids_joined)

        rows = con.execute(sql)

        food_list = []
        for row in rows:
            external_id = row[8]
            category_id = row[9]
            place_type = row[10]
            slug = row[11]
            food_list.append(FoodDto(
                id=row[0],
                name=row[1],
                src=row[2],
                price=row[3],
                restaurant_name=row[4],
                address=row[5],
                weight=row[6],
                rating=row[7],
                link=build_link_ovverriden(slug, category_id, external_id, place_type)
            ))

        return food_list


def find_restaurant(xs, restaurant_id):
    for x in xs:
        if x.slug == restaurant_id:
            return x
    return None


def build_link_ovverriden(slug, category_id, external_id, place_type):
    if place_type == PlaceType.restaurant:
        return "https://eda.yandex.ru/moscow/r/{}?category={}&item={}&placeSlug={}".format(slug,
                                                                                           category_id,
                                                                                           external_id,
                                                                                           slug)
    else:
        return "https://eda.yandex.ru/retail/{}/product/{}?placeSlug={}".format(slug, external_id,
                                                                                slug)


def build_link(vo: FoodVO, restaurant: RestaurantVO):
    if restaurant.place_type == PlaceType.restaurant:
        return "https://eda.yandex.ru/moscow/r/{}?category={}&item={}&placeSlug={}".format(restaurant.slug,
                                                                                           vo.category_id,
                                                                                           vo.external_id,
                                                                                           restaurant.slug)
    else:
        return "https://eda.yandex.ru/retail/{}/product/{}?placeSlug={}".format(vo.restaurant_id, vo.external_id,
                                                                                vo.restaurant_id)
