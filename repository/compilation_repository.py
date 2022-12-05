from sqlalchemy.orm import Session

from config import database
from model.compilation import CompilationVO, CompilationDto, CompilationResponse


def find(session: Session, email: str, name: str):
    stmt = session.query(CompilationVO) \
        .filter(CompilationVO.account_email.ilike(email))\
        .filter(CompilationVO.name.ilike(name))
    print(stmt)
    return stmt.first()


def find_all(session: Session, email: str):
    return session.query(CompilationVO) \
        .filter(CompilationVO.account_email.ilike(email)) \
        .all()


def find_all_joined(session: Session, email: str):
    all = session.query(CompilationVO) \
        .filter(CompilationVO.account_email.ilike(email)) \
        .all()

    result = []
    for x in all:
        values = x.values.split(", ")
        for value in values:
            result.append(value)
    return result


def add_item(session: Session, email: str, food_id: int, name = "Избранное"):
    vo = find(session, email, name)

    if vo is None:
        vo = CompilationVO(
            account_email=email,
            name=name,
            values=str(food_id)
        )
    else:
        vo.values = vo.values + ", " + str(food_id)
    session.add(vo)
    session.commit()


def fix(session: Session):
    all = session.query(CompilationVO).all()
    for vo in all:
        xs = vo.values.split(", ")
        try:
            xs.remove("")
            vo.values = ", ".join(xs)
            session.add(vo)
        except:
            print("x in not in list: {}".format(xs))
    session.commit()


def remove_item(session: Session, email: str, name: str, food_id: int):
    vo = find(session, email, name)
    values = vo.values.split(", ")
    values.remove(str(food_id))
    vo.values = ", ".join(values)
    session.add(vo)
    session.commit()


def remove_compilation(session: Session, email: str, name: str):
    vo = find(session, email, name)
    session.delete(vo)
    session.commit()
