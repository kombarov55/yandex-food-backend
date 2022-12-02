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


class SearchFoodResponse(pydantic.BaseModel):
    lowest_price_food_list: list[FoodDto]
    highest_price_food_list: list[FoodDto]
    biggest_weight_food_list: list[FoodDto]
    avg_price: int
    chart_data: list[FoodChartDto]


