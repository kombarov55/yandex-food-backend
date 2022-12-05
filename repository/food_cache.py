from pathlib import Path

import pydantic

from model.search_food import SearchFoodResponse


def exists(food_name: str):
    filename = "cache/{}.json".format(food_name)
    file = Path(filename)
    return file.exists()


def save(food_name: str, rs: SearchFoodResponse):
    with open("cache/{}.json".format(food_name), "w") as file:
        file.write(rs.json())


def get(food_name: str):
    return pydantic.parse_file_as(path="cache/{}.json".format(food_name), type_=SearchFoodResponse)
