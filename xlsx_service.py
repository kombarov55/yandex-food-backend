import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from model.restaurant import RestaurantVO


def to_csv(restaurant_list: list, food_list: list, path: str):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    write_header(worksheet, workbook)
    row = 1
    for food in food_list:
        restaurant: RestaurantVO = find_restaurant(restaurant_list, food.restaurant_id)

        col = 0

        worksheet.write(row, col, restaurant.slug)
        col += 1
        worksheet.write(row, col, restaurant.name)
        col += 1
        worksheet.write(row, col, restaurant.rating)
        col += 1
        worksheet.write(row, col, restaurant.delivery_time)
        col += 1
        worksheet.write(row, col, restaurant.address)
        col += 1
        worksheet.write(row, col, restaurant.latitude + ", " + restaurant.longitude)
        col += 1
        worksheet.write(row, col, food.name)
        col += 1
        worksheet.write(row, col, food.description)
        col += 1
        worksheet.write(row, col, food.price)
        col += 1
        worksheet.write(row, col, food.weight)
        col += 1
        row += 1

    workbook.close()


def write_header(worksheet: Worksheet, workbook: Workbook):
    bold = workbook.add_format({"bold": True})
    col = 0

    worksheet.write(0, col, "slug ресторана", bold)
    col += 1
    worksheet.write(0, col, "Название ресторана", bold)
    col += 1
    worksheet.write(0, col, "Рейтинг", bold)
    col += 1
    worksheet.write(0, col, "Время доставки", bold)
    col += 1
    worksheet.write(0, col, "Адрес", bold)
    col += 1
    worksheet.write(0, col, "Координаты", bold)
    col += 1
    worksheet.write(0, col, "Название блюда", bold)
    col += 1
    worksheet.write(0, col, "Описание", bold)
    col += 1
    worksheet.write(0, col, "Цена", bold)
    col += 1
    worksheet.write(0, col, "Вес", bold)
    col += 1


def find_restaurant(xs, restaurant_id):
    for x in xs:
        if x.slug == restaurant_id:
            return x
    return None
