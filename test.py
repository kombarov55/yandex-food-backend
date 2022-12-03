from pprint import pprint

from config import database
from model.food import FoodVO
from repository import food_repository


def test_lowest_price(session):
    return food_repository.search_lowest_price_food(session, "цезарь", 1, 5)

def test_highest_price(session):
    return food_repository.search_highest_price_food(session, "цезарь", 1, 5)


def test_biggest_weight(session):
    return food_repository.search_biggest_weight_food(session, "цезарь", 1, 5)


def test_con():
    with database.engine.connect() as con:
        sql = "select name, src, price, weight, restaurant_id, external_id " \
              "from food " \
              "where xlsx_request_id = 1 " \
              "and (" \
              "name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'" \
              ") "

        rows = con.execute(sql, name="Цезарь", lower_name="цезарь")

        food_list = []
        for row in rows:
            food_list.append(FoodVO(
                name=row[0],
                src=row[1],
                price=row[2],
                weight=row[3],
                restaurant_id=row[4],
                external_id=row[5]
            ))
    pprint(len(food_list))


if __name__ == "__main__":
    session = database.session_local()
    result = test_lowest_price(session)
    print(len(result))
    pprint(result)

    result = test_highest_price(session)
    print(len(result))
    pprint(result)

    result = test_biggest_weight(session)
    print(len(result))
    pprint(result)

    test_con()
