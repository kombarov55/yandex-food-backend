from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from config import database


class RestaurantVO(database.base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True)
    xlsx_request_id = Column(Integer, index=True)
    slug = Column(String)
    name = Column(String)
    src = Column(String)
    rating = Column(Float)
    rating_count = Column(Integer)
    delivery_time = Column(String)
    address = Column(String)
    longitude = Column(String)
    latitude = Column(String)
    open_at = Column(String)
    close_at = Column(String)
    place_type = Column(String)


class PlaceType:
    restaurant = "restaurant"
    shop = "shop"
