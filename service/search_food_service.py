from config import database
from model.restaurant import PlaceType
from model.search_food import SearchFoodResponse, FoodDto, FoodChartDto, RestaurantDto, HighlightedRestaurantDto, \
    SearchFoodResponseItem
from repository import food_repository, restaurant_repository


def find(food_name: str):
    session = database.session_local()
    amount = 5
    restaurants = restaurant_repository.find_restaurants_by_serving_food_name(session, food_name)

    return SearchFoodResponse(
        by_restaurant=search_food_response_item(session, food_name, amount, restaurants, PlaceType.restaurant),
        by_shop=search_food_response_item(session, food_name, amount, restaurants, PlaceType.shop)
    )


def search_food_response_item(session, food_name, amount, restaurants, place_type):
    return SearchFoodResponseItem(
            lowest_price_food_list=food_repository.search_lowest_price_food(session, food_name, restaurants, amount),
            highest_price_food_list=food_repository.search_highest_price_food(session, food_name, restaurants, amount),
            biggest_weight_food_list=food_repository.search_biggest_weight_food(session, food_name, restaurants, amount),
            avg_price=food_repository.search_avg_price(session, food_name, 1),
            chart_data=food_repository.get_chart_data(food_name, restaurants),
            restaurants=restaurant_repository.find_and_format_for_placemark(session, 1),
            best_highlighted_restaurant=restaurant_repository.get_best_rating_restaurant(session, 1),
            worst_highlighted_restaurant=restaurant_repository.get_worst_rating_restaurant(session, 1),
            best_choice_food_list=food_repository.find_best_food(restaurants, food_name, amount)
        )


def stub_search_food_response_item():
    return SearchFoodResponseItem(
        lowest_price_food_list=[
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="She", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p",
                    restaurant_name="Grape wine & kitchen",
                    address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4")
        ],
        highest_price_food_list=[
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4")
        ],
        biggest_weight_food_list=[
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4")
        ],
        avg_price=666,
        chart_data=generate_chart_data(),
        restaurants=[
            RestaurantDto(
                name="Right Brewery",
                address="Большая набережная вл. Ленина д. 14",
                longitude=55.744589,
                latitude=37.613065,
                rating=5,
                rating_count=10
            )
        ],
        best_highlighted_restaurant=HighlightedRestaurantDto(
            name="Лучший ресторан города",
            src="https://eda.yandex/images/3724421/7ccfd22d1f539f88212eb1b2f219f6eb-100x100.jpg",
            address="Москва ул. Ленина 5",
            rating=4.9,
            rating_count=100000
        ),
        worst_highlighted_restaurant=HighlightedRestaurantDto(
            name="Худшая дыра города",
            src="https://eda.yandex/images/3513074/b6e1ad87e2de180003818a23c25c57f1-100x100.jpg",
            address="Москва ул. Вавилова д. 3",
            rating=1.3,
            rating_count=666666
        ),
        best_highlighted_shop=HighlightedRestaurantDto(
            name="Пятерочка",
            address="Москва ул. Ленина 5",
            src="https://eda.yandex/images/3513074/b6e1ad87e2de180003818a23c25c57f1-100x100.jpg",
            rating=4.9,
            rating_count=100000
        ),
        worst_highlighted_shop=HighlightedRestaurantDto(
            name="Продукты 'У Ашота'",
            src="https://eda.yandex/images/3513074/b6e1ad87e2de180003818a23c25c57f1-100x100.jpg",
            address="Москва ул. Вавилова д. 3",
            rating=1.3,
            rating_count=666666
        ),
        best_choice_food_list=[
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="She", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p",
                    restaurant_name="Grape wine & kitchen",
                    address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
            FoodDto(name="Том ям с креветками",
                    src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",
                    price="680p", restaurant_name="Grape wine & kitchen", address="Большая Никитская улица, 15с1",
                    description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4")
        ]
    )


def generate_chart_data():
    result = []

    for i in range(0, 30):
        xs = [
            FoodChartDto(shop_name="She", price=680),
            FoodChartDto(shop_name="Сакура", price=449),
            FoodChartDto(shop_name="Grape wine & kitchen", price=790),
            FoodChartDto(shop_name="Pho Oanh", price=485)
        ]
        for x in xs:
            result.append(x)

    result.sort(key=lambda x: x.price)

    return result
