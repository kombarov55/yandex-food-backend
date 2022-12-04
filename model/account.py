import pydantic
from sqlalchemy import Column, Integer, String

from config import database


class AccountVO(database.base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)


class AuthRs(pydantic.BaseModel):
    success: bool
    error_msg: str = None
    email: str
