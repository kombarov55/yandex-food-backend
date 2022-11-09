from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import database


class RestaurantVO(database.base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    food_items = relationship("FoodVO", back_populates="restaurant")
