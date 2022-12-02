from model.search_food import SearchFoodResponse, FoodDto, FoodChartDto, RestaurantDto, HighlightedRestaurantDto


def find(food_name: str):
    return SearchFoodResponse(
        lowest_price_food_list=[
            FoodDto(name="Том ям с креветками",src="https://eda.yandex/images/2794391/9604ef0615a2a914cb22a1ac9f47b4e4-400x400nocrop.jpeg",price="680p",restaurant_name="She",address="Большая Никитская улица, 15с1",description="Классический пряный острый суп том ям с креветками, грибами шиитаке, помидорами черри, кинзой и кокосовым молоком. Бульон том ям: куриный бульон, свежая морковь, лук репчатый, корень галангала, лимонник, перец чили, кинза, корень имбиря, листья лайма.На 100 граммов: К 95, Б 6, Ж 6, У 4"),
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
            address="Москва ул. Ленина 5",
            rating=4.9,
            rating_count=100000
        ),
        worst_highlighted_restaurant=HighlightedRestaurantDto(
            name="Худшая дыра города",
            address="Москва ул. Вавилова д. 3",
            rating=1.3,
            rating_count=666666
        ),
        best_highlighted_shop=HighlightedRestaurantDto(
            name="Пятерочка",
            address="Москва ул. Ленина 5",
            rating=4.9,
            rating_count=100000
        ),
        worst_highlighted_shop=HighlightedRestaurantDto(
            name="Продукты 'У Ашота'",
            address="Москва ул. Вавилова д. 3",
            rating=1.3,
            rating_count=666666
        )
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
