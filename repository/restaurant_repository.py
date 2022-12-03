from sqlalchemy import exists
from sqlalchemy.orm import Session

from config import database
from model.restaurant import RestaurantVO, PlaceType
from model.search_food import RestaurantDto, HighlightedRestaurantDto


def save(session: Session, restaurant: RestaurantVO):
    result = session.query(RestaurantVO).filter(RestaurantVO.slug == restaurant.slug).first()

    if result is None:
        session.add(restaurant)
        session.commit()
        session.refresh(restaurant)
        return restaurant
    else:
        return result


def find_all(session: Session, xlsx_request_id: int):
    return session.query(RestaurantVO).filter(RestaurantVO.xlsx_request_id == xlsx_request_id).all()


def find_restaurants_by_serving_food_name(session: Session, food_name: str):
    with database.engine.connect() as con:
        sql = "select distinct restaurant_id " \
              "from food " \
              "where name like :name || '%' " \
              "or name like '%' || :name || '%' " \
              "or name like :lower_name || '%' " \
              "or name like '%' || :lower_name || '%'"

        rows = con.execute(sql, name=food_name.capitalize(), lower_name=food_name.lower())

        slug_list = []
        for row in rows:
            slug_list.append(row[0])

    return session.query(RestaurantVO).filter(RestaurantVO.slug.in_(slug_list)).all()


def find_and_format_for_placemark(session: Session, xlsx_request_id: int):
    restaurants = find_all(session, xlsx_request_id)
    return list(map(lambda x: RestaurantDto(
        name=x.name,
        address=x.address,
        longitude=x.longitude,
        latitude=x.latitude,
        rating=x.rating,
        rating_count=x.rating_count,
        open_at=x.open_at,
        close_at=x.close_at,
        link=build_link(x),
        delivery_time=x.delivery_time
    ), restaurants))


def get_best_rating_restaurant(session: Session, xlsx_reuqest_id: int):
    first = session.query(RestaurantVO)\
        .filter(RestaurantVO.xlsx_request_id == xlsx_reuqest_id)\
        .filter(RestaurantVO.rating.isnot(None))\
        .order_by(RestaurantVO.rating.desc())\
        .first()

    return convert_to_highlighted_dto(first)


def get_worst_rating_restaurant(session: Session, xlsx_reuqest_id: int):
    first = session.query(RestaurantVO)\
        .filter(RestaurantVO.xlsx_request_id == xlsx_reuqest_id) \
        .filter(RestaurantVO.rating.isnot(None)) \
        .order_by(RestaurantVO.rating.asc())\
        .first()

    return convert_to_highlighted_dto(first)


def convert_to_highlighted_dto(x: RestaurantVO):
    return HighlightedRestaurantDto(
        name=x.name,
        src=x.src,
        address=x.address,
        rating=x.rating,
        rating_count=x.rating_count,
        href=build_link(x),
        open_at=x.open_at,
        close_at=x.close_at
    )

def build_link(vo: RestaurantVO):
    if vo.place_type == PlaceType.restaurant:
        return "https://eda.yandex.ru/moscow/r/{}?placeSlug={}&shippingType=delivery".format(vo.slug, vo.slug)

    return "https://eda.yandex.ru/retail/{}?placeSlug=".format(vo.slug, vo.slug)


def delete_by_xlsx_request_id(session: Session, xlsx_request_id: int):
    session.query(RestaurantVO).filter(RestaurantVO.xlsx_request_id == xlsx_request_id).delete()
    session.commit()
