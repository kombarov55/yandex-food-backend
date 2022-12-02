import pydantic


class FoodDto(pydantic.BaseModel):
    name: str
    src: str
    price: str
    restaurant_name: str
    address: str
    description: str
    weight: str = 449
    link: str = "https://eda.yandex.ru/retail/vkusvill/product/a4c5012a-703c-4d1b-8be3-c02dc323ab98?placeSlug=vkusvill_marosejka_2_15s1_rmxdp"


class FoodChartDto(pydantic.BaseModel):
    shop_name: str
    price: float


class RestaurantDto(pydantic.BaseModel):
    name: str
    address: str
    longitude: float
    latitude: float
    rating: float
    rating_count: int
    open_at: str = "08:00"
    close_at: str = "23:00"
    link: str = "https://eda.yandex.ru/retail/vkusvill/product/a4c5012a-703c-4d1b-8be3-c02dc323ab98?placeSlug=vkusvill_marosejka_2_15s1_rmxdp"


class HighlightedRestaurantDto(pydantic.BaseModel):
    name: str
    src: str
    address: str
    rating: float
    rating_count: int
    href: str = "https://eda.yandex.ru/retail/vkusvill/product/a4c5012a-703c-4d1b-8be3-c02dc323ab98?placeSlug=vkusvill_marosejka_2_15s1_rmxdp"


class SearchFoodResponseItem(pydantic.BaseModel):
    lowest_price_food_list: list
    highest_price_food_list: list
    biggest_weight_food_list: list
    avg_price: float
    chart_data: list
    restaurants: list
    best_highlighted_restaurant: HighlightedRestaurantDto
    worst_highlighted_restaurant: HighlightedRestaurantDto
    best_highlighted_shop: HighlightedRestaurantDto
    worst_highlighted_shop: HighlightedRestaurantDto
    best_choice_food_list: list


class SearchFoodResponse(pydantic.BaseModel):
    by_restaurant: SearchFoodResponseItem
    by_shop: SearchFoodResponseItem
