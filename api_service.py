import requests

from model.food import FoodVO, PlaceType
from model.restaurant import RestaurantVO
from model.xlsx_request import XlsxRequestVO


def load_restaurant_food(slug: str, restaurant_id, xlsx_request_vo: XlsxRequestVO):
    print("loading food for /r slug={}".format(slug))

    url = "https://eda.yandex.ru/api/v2/menu/retrieve/{}".format(slug)
    res = requests.get(url)
    json = res.json()
    categories = json["payload"]["categories"]
    result = []
    for category in categories:
        category_id = get_field(category, "id")
        items = category["items"]
        for item in items:
            result.append(FoodVO(
                xlsx_request_id=xlsx_request_vo.id,
                name=get_field(item, "name"),
                description=get_field(item, "description"),
                price=int(get_field(item, "price")),
                weight=parse_weight(item),
                src="https://eda.yandex./" + query(item, "picture.uri", "").replace("{w}", "400").replace("{h}", "400"),
                restaurant_id=restaurant_id,
                external_id=get_field(item, "id"),
                category_id=category_id,
                place_type=PlaceType.restaurant
            ))
    print("slug={} len(result)={}".format(slug, len(result)))
    return result


def load_retail_food(category_ids: list, slug, xlsx_request_vo: XlsxRequestVO):
    print("loading food for /retail slug={}".format(slug))

    result = []
    for category_id in category_ids:
        url = "https://eda.yandex.ru/api/v2/menu/goods"
        body = {"slug": slug, "category": category_id, "filters": {}, "maxDepth": 100}
        rs = requests.post(url, json=body)
        try:
            json = rs.json()

            categories = json["payload"]["categories"]
            for category in categories:
                items = category["items"]
                if len(items) != 0:
                    for item in items:
                        src = query(item, "picture.url", "").replace("{w}", "400").replace("{h}", "400")
                        vo = FoodVO(
                            xlsx_request_id=xlsx_request_vo.id,
                            restaurant_id=slug,
                            name=get_field(item, "name"),
                            description=get_field(item, "description"),
                            price=int(get_field(item, "price")),
                            weight=parse_weight(item),
                            src=src,
                            external_id=get_field(item, "public_id"),
                            place_type=PlaceType.shop
                        )
                        result.append(vo)
        except:
            print("failed to POST:")
            print("POST {}".format(url))
            print(body)
            print("response ({}): ".format(rs.status_code))
            print(rs.content)

        print("slug={} len(result)={}".format(slug, len(result)))
        return result


def load_retail_info(slug):
    rs = requests.get("https://eda.yandex.ru/api/v2/catalog/{}".format(slug))
    json = rs.json()

    found_place = json["payload"]["foundPlace"]

    delivery_time = ""

    location_params = found_place["locationParams"]
    if location_params is not None:
        delivery_time = location_params["deliveryTime"]["min"] + "-" + location_params["deliveryTime"]["max"],

    src = query(json, "payload.foundPlace.place.picture.uri")
    if src is not None:
        src = "https://eda.yandex/" + src.replace("{w}", "400").replace("{h}", "400")

    rating = query(json, "payload.foundPlace.place.rating", None)
    if rating is not None:
        rating = float(rating)

    return RestaurantVO(
        slug=slug,
        name=query(json, "payload.foundPlace.place.name"),
        src=src,
        rating=rating,
        rating_count=int(query(json, "payload.foundPlace.place.ratingCount", 0)),
        delivery_time=delivery_time,
        address=query(json, "payload.foundPlace.place.address.short"),
        longitude=query(json, "payload.foundPlace.place.address.location.longitude"),
        latitude=query(json, "payload.foundPlace.place.address.location.latitude"),
        place_type="shop"
    )


def parse_weight(item: dict):
    weight_str = get_field(item, "weight")

    if weight_str is None:
        return None

    if weight_str.lower().endswith("г") or weight_str.lower().endswith("мл"):
        return float(weight_str.split(' ')[0].replace(",", "."))
    if weight_str.lower().endswith("л") or weight_str.lower().endswith("кг"):
        return float(weight_str.split(' ')[0].replace(",", ".")) * 1000


def query(obj, keys_str: str, default=None):
    keys = keys_str.split(".")
    for key in keys:
        try:
            obj = obj[key]
        except KeyError:
            return default
    return obj


def get_field(item: dict, name: str):
    if name in item:
        return str(item[name])
    else:
        return None


def get_nested_field(item, name1, name2):
    if name1 in item:
        nested = item[name1]
        if nested is not None and name2 in nested:
            return nested[name2]
        else:
            return None
    else:
        return None
