from pprint import pprint

from config import database
from repository import food_repository


def test_lowest_price(session):
    return food_repository.search_lowest_price_food(session, "цезарь", 1, 5)

if __name__ == "__main__":
    session = database.session_local()
    print(len(test_lowest_price(session)))