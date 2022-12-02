import pydantic


class FoodDto:
    name: str
    src: str
    price: str
    restaurant_name: str
    address: str
    description: str
    weight: str = "449г"


class FoodChartDto:
    shop_name: str
    price: int


class SearchFoodResponse:
    lowest_price_food_list: list
    highest_price_food_list: list
    biggest_weight_food_list: list
    avg_price: int
    chart_data: list


