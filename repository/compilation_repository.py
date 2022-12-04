from sqlalchemy.orm import Session

from model.compilation import CompilationVO


def find(session: Session, email: str, name: str):
    return session.query(CompilationVO) \
        .filter(CompilationVO.account_email.ilike(email))\
        .filter(CompilationVO.name.ilike(name)) \
        .first()


def add_item(session: Session, email: str, food_id: int):
    vo = find(session, email, "Избранное")

    if vo is None:
        vo = CompilationVO(
            account_email=email,
            name="Избранное",
            values=str(food_id)
        )
    else:
        vo.values = vo.values + ", " + str(food_id)
    session.add(vo)
    session.commit()


def remove_item(session: Session, email: str, name: str, food_id: int):
    vo = find(session, email, name)
    values = vo.values.split(", ")
    values.remove(str(food_id))
    vo.values = ", ".join(values)
    session.add(vo)
    session.commit()
