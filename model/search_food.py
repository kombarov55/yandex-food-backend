import pydantic


class FoodDto(pydantic.BaseModel):
    name: str
    src: str
    price: str = None
    restaurant_name: str
    address: str
    weight: float = None
    link: str = "https://eda.yandex.ru/retail/vkusvill/product/a4c5012a-703c-4d1b-8be3-c02dc323ab98?placeSlug=vkusvill_marosejka_2_15s1_rmxdp"


class FoodChartDto(pydantic.BaseModel):
    shop_name: str
    price: float


class RestaurantDto(pydantic.BaseModel):
    name: str
    address: str
    longitude: float = None
    latitude: float = None
    rating: float = None
    rating_count: int = None
    open_at: str = None
    close_at: str = None
    link: str = "https://eda.yandex.ru/retail/vkusvill/product/a4c5012a-703c-4d1b-8be3-c02dc323ab98?placeSlug=vkusvill_marosejka_2_15s1_rmxdp"
    delivery_time: str = None


class HighlightedRestaurantDto(pydantic.BaseModel):
    name: str
    src: str
    address: str = None
    rating: float = None
    rating_count: int = None
    open_at: str = None
    close_at: str = None
    href: str


class SearchFoodResponseItem(pydantic.BaseModel):
    lowest_price_food_list: list = None
    highest_price_food_list: list = None
    biggest_weight_food_list: list = None
    avg_price: float = None
    chart_data: list = None
    restaurants: list = None
    best_highlighted_restaurant: HighlightedRestaurantDto = None
    worst_highlighted_restaurant: HighlightedRestaurantDto = None
    best_choice_food_list: list = None


class SearchFoodResponse(pydantic.BaseModel):
    by_restaurant: SearchFoodResponseItem
    by_shop: SearchFoodResponseItem
