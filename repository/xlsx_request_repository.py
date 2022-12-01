from datetime import datetime

from sqlalchemy.orm import Session

from model.xlsx_request import XlsxRequestVO, XlsxRequestStatus


def create(session: Session, food_name: str):
    vo = XlsxRequestVO(
        status=XlsxRequestStatus.not_started,
        start_date=datetime.now(),
        food_name=food_name
    )
    session.add(vo)
    session.commit()
    session.refresh(vo)
    return vo


def find_not_started(session: Session):
    return session.query(XlsxRequestVO).filter(XlsxRequestVO.status == XlsxRequestStatus.not_started).all()


def get_all(session: Session):
    return session.query(XlsxRequestVO).all()


def update(session: Session, vo: XlsxRequestVO):
    vo_from_db = session.get(XlsxRequestVO, vo.id)
    vo_from_db.status = vo.status
    vo_from_db.end_date = vo.end_date
    vo_from_db.filename = vo.filename
    vo_from_db.what_is_doing = vo.what_is_doing
    session.add(vo_from_db)
    session.commit()
    session.refresh(vo_from_db)
    return vo_from_db


def set_what_is_doing(session: Session, vo: XlsxRequestVO, s: str):
    vo.what_is_doing = s
    update(session, vo)
