import pydantic
from sqlalchemy import Column, Integer, String

from config import database


class CompilationVO(database.base):
    __tablename__ = "compilation"

    id = Column(Integer, primary_key=True, index=True)
    account_email = Column(String, index=True)
    name = Column(String)
    values = Column(String)


class CompilationResponse(pydantic.BaseModel):
    payload: list


class CompilationDto(pydantic.BaseModel):
    id: int
    name: str
    food_list: list
