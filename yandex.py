import time
import urllib
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from config import database
from model.restaurant import RestaurantVO
from repository import restaurant_repository, food_repository
from service import api_service

database.base.metadata.drop_all(bind=database.engine)
database.base.metadata.create_all(bind=database.engine)
session = database.session_local()


def set_location():
    page.wait_for_selector("(//h2[@class='DesktopHeaderBlock_headerText DesktopHeaderBlock_headerTextBold'])[1]")
    location_text = page.locator("span.DesktopAddressButton_address").inner_text()
    if location_text == "Укажите адрес доставки":
        page.locator("button.DesktopHeader_addressButton").click()
    else:
        page.locator("button.DesktopUIButton_root").click()
        page.locator("div.UIPopupList_option").click()
    # page.click("svg.AppAddressInput_closeIcon");
    page.wait_for_selector(".DesktopLocationModal_wrapper")
    input_locator = page.locator("input.AppAddressInput_addressInput")
    input_locator.type("Москва, Красная площадь 3")
    page.click("div.react-autosuggest__suggestions-container")
    page.click("button.DesktopLocationModal_ok")
    page.wait_for_selector(
        "//span[@class='DesktopAddressButton_addressStreet' and contains(text(), 'Красная площадь')]")


def search(food_name):
    page.goto("https://eda.yandex.ru/search?query={}&type=all".format(food_name))
    page.wait_for_selector("//h1[contains(text(),'Найден')]")


def parse_all_shops():
    page.wait_for_load_state(state="networkidle")
    scroll_slowly_to_bottom()
    hrefs = get_hrefs()
    for href in hrefs:
        slug = get_query_param(href, "placeSlug")
        is_retail = href.startswith("/retail")
        page.goto("https://eda.yandex.ru/{}".format(href))
        page.wait_for_load_state(state="networkidle")

        if not is_retail:
            parse_restaurant(slug)
        else:
            parse_shop(slug)


def parse_restaurant(slug):
    page.click("//button[@class='RestaurantHeader_badge']//*[name()='svg']")
    page.wait_for_selector("div.AppPopup_wrapper")
    restaurant_name = page.locator(
        "//h3[@class='UiKitText_root UiKitText_Title4 UiKitText_Bold UiKitText_Text']").inner_text()

    vo = RestaurantVO(name=restaurant_name)
    restaurant_repository.save(session, vo)

    address = page.locator("//span[@class='RestaurantPopup_infoAddr']").inner_text()
    print("{} {} {}".format(slug, restaurant_name, address))
    food_list = api_service.load_restaurant_food(slug, slug)
    food_repository.save_all(session, food_list)


def parse_shop(slug):
    vo = RestaurantVO(name=slug)
    restaurant_repository.save(session, vo)
    category_ids = get_retail_category_ids()
    food_list = api_service.load_retail_food(category_ids, slug)
    food_repository.save_all(session, food_list)


def get_retail_category_ids() -> list[int]:
    a_els = page.locator("a.UiKitDesktopShopMenuItem_menuLink")
    result = []
    for i in range(0, a_els.count()):
        a = a_els.nth(i)
        href = a.get_attribute("href")
        parse_result = urlparse(href)
        path_splitted = parse_result.path.split("/")
        category_id = path_splitted[len(path_splitted) - 1]
        result.append(int(category_id))
    return result


def get_hrefs():
    a_els = page.locator("a.DesktopSearchPlaceCarousel_link")
    result = []
    for i in range(0, a_els.count()):
        result.append(a_els.nth(i).get_attribute("href"))
    return result


def scroll(y):
    page.evaluate("window.scrollTo(0, {})".format(y))


def get_query_param(url, param):
    q = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(q.query)[param][0]


def scroll_slowly_to_bottom():
    current_height = 0
    delta = 500

    while True:
        page.evaluate("() => window.scrollTo(0, {});".format(current_height + delta))
        current_height += delta
        time.sleep(0.1)
        page_height = page.evaluate("() => document.body.scrollHeight;")
        if current_height > page_height:
            break


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://eda.yandex.ru/moscow?shippingType=delivery")
    set_location()
    search("тоблерон")
    parse_all_shops()
    page.pause()
