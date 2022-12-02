from sqlalchemy.sql import exists
from sqlalchemy.orm import Session

from model.account import AccountVO, AuthRs


def register(session: Session, body: dict):
    email_exists = session.query(exists().where(AccountVO.email == body["email"])).scalar()
    if email_exists:
        return AuthRs(
            success=False,
            error_msg="Email уже зарегистрирован",
            email=body["email"]
        )
    vo = AccountVO(
        email=body["email"],
        password=body["password"],
        name=body["name"]
    )
    session.add(vo)
    session.commit()
    return AuthRs(
        success=True,
        email=body["email"]
    )


def login(session: Session, body: dict):
    first = session.query(AccountVO).filter(AccountVO.email == body["email"]).filter(
        AccountVO.password == body["password"]).first()

    if first is None:
        return AuthRs(
            success=False,
            error_msg="Неправильный логин или пароль",
            email=body["email"]
        )
    else:
        return AuthRs(
            success=True,
            email=body["email"]
        )
