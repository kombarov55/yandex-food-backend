import pydantic


class FoodDto(pydantic.BaseModel):
    name: str
    src: str
    price: str
    restaurant_name: str
    address: str
    description: str
    weight: str = "449г"


class FoodChartDto(pydantic.BaseModel):
    shop_name: str
    price: int


class RestaurantDto(pydantic.BaseModel):
    name: str
    address: str
    longitude: float
    latitude: float
    rating: float
    rating_count: int


class HighlightedRestaurantDto(pydantic.BaseModel):
    name: str
    address: str
    rating: float
    rating_count: int


class SearchFoodResponse(pydantic.BaseModel):
    lowest_price_food_list: list
    highest_price_food_list: list
    biggest_weight_food_list: list
    avg_price: int
    chart_data: list
    restaurants: list
    best_highlighted_restaurant: HighlightedRestaurantDto
    worst_highlighted_restaurant: HighlightedRestaurantDto
    best_highlighted_shop: HighlightedRestaurantDto
    worst_highlighted_shop: HighlightedRestaurantDto



