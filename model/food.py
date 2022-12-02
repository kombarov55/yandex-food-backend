from sqlalchemy import Column, Integer, String, Float

from config import database


class FoodVO(database.base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String)
    category_id = Column(String)
    restaurant_id = Column(Integer, index=True)
    xlsx_request_id = Column(Integer, index=True)
    name = Column(String)
    description = Column(String)
    src = Column(String)
    price = Column(Integer)
    weight = Column(Float)
    place_type = Column(String)


class PlaceType:
    restaurant = "restaurant"
    shop = "shop"

