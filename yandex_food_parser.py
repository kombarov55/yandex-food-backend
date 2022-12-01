import time
import urllib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Page
from sqlalchemy.orm import Session

import api_service
import screenshot_util
import solve_captcha
import xlsx_service
from config import database, app_config
from model.restaurant import RestaurantVO
from model.xlsx_request import XlsxRequestVO, XlsxRequestStatus
from repository import restaurant_repository, food_repository, xlsx_request_repository


def set_location(page: Page):
    # page.wait_for_selector("(//h2[@class='DesktopHeaderBlock_headerText DesktopHeaderBlock_headerTextBold'])[1]")
    page.wait_for_load_state("networkidle")
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


def search(page, food_name):
    page.goto("https://eda.yandex.ru/search?query={}&type=all".format(food_name))
    page.wait_for_selector("//h1[contains(text(),'Найден')]")


def parse_all_shops(page, session, vo: XlsxRequestVO):
    page.wait_for_load_state(state="networkidle")

    print("starting scrolling to bottom")
    xlsx_request_repository.set_what_is_doing(session, vo, "Скролим вниз, до конца страницы")
    scroll_slowly_to_bottom(page)
    print("end scrolling to bottom")

    xlsx_request_repository.set_what_is_doing(session, vo, "Получаем все ссылки на магазины")
    hrefs = get_hrefs(page)
    print("parsed hrefs: {}".format(hrefs))

    for i in range(0, len(hrefs)):
        href = hrefs[i]
        slug = get_query_param(href, "placeSlug")
        is_retail = href.startswith("/retail")
        page.goto("https://eda.yandex.ru/{}".format(href))
        page.wait_for_load_state(state="networkidle")

        xlsx_request_repository.set_what_is_doing(session, vo,
                                                  "Парсим {} (прогресс: {}/{})".format(slug, i, len(hrefs)))

        if not is_retail:
            print("parsing restaurant slug={}".format(slug))
            parse_restaurant(page, session, slug, vo)
        else:
            print("parsing shop slug={}".format(slug))
            parse_shop(session, page, slug, vo)


def parse_restaurant(page, session, slug, xlsx_request_vo: XlsxRequestVO):
    page.wait_for_selector("li.RestaurantCategories_item")
    time.sleep(1)

    if page.locator("div.Modal_modalWrapper").is_visible():
        page.click("div.ModalSurge_button")

    restaurant_name = page.locator("h1.RestaurantHeader_name").inner_text()
    rich_badges = page.locator("button.RestaurantHeader_richBadge")

    delivery_time = ""

    if rich_badges.count() == 2:
        delivery_badge = rich_badges.nth(0)
        delivery_time = delivery_badge.locator("div.RestaurantHeader_badgeTopLine").inner_text()

        rating_badge = rich_badges.nth(1)
        rating = rating_badge.locator("div.RestaurantHeader_badgeTopLine").inner_text()
        rating_count = rating_badge.locator("div.RestaurantHeader_badgeBottomLine").inner_text()
    else:
        rating_badge = rich_badges.nth(0)
        rating = rating_badge.locator("div.RestaurantHeader_badgeTopLine").inner_text()
        rating_count = rating_badge.locator("div.RestaurantHeader_badgeBottomLine").inner_text()

    page.click("button.RestaurantHeader_badge")
    page.wait_for_selector("div.RestaurantPopup_infoPopup")

    address = page.locator("span.RestaurantPopup_infoAddr").inner_text()

    vo = RestaurantVO(
        xlsx_request_id=xlsx_request_vo.id,
        slug=slug,
        name=restaurant_name,
        rating=rating,
        rating_count=rating_count,
        delivery_time=delivery_time,
        address=address
    )
    print(f"{restaurant_name} {rating} {rating_count} {delivery_time} {address}")
    restaurant_repository.save(session, vo)
    food_list = api_service.load_restaurant_food(slug, slug, xlsx_request_vo)
    food_repository.save_all(session, food_list)
    print("saved {} items for restaurant_name={} slug={}".format(len(food_list), restaurant_name, slug))


def parse_shop(session, page, slug, xlsx_request_vo: XlsxRequestVO):
    vo = api_service.load_retail_info(slug)
    vo.xlsx_request_id = xlsx_request_vo.id
    restaurant_repository.save(session, vo)

    category_ids = get_retail_category_ids(page)
    food_list = api_service.load_retail_food(category_ids, slug, xlsx_request_vo)
    food_repository.save_all(session, food_list)
    print("parsed {} items for shop_name={} slug={}".format(len(food_list), vo.name, vo.slug))


def get_retail_category_ids(page):
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


def get_hrefs(page):
    a_els = page.locator("a.DesktopSearchPlaceCarousel_link")
    result = []
    for i in range(0, a_els.count()):
        result.append(a_els.nth(i).get_attribute("href"))
    return result


def scroll(page, y):
    page.evaluate("window.scrollTo(0, {})".format(y))


def get_query_param(url, param):
    q = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(q.query)[param][0]


def scroll_slowly_to_bottom(page):
    current_height = 0
    delta = 500

    while True:
        page.evaluate("() => window.scrollTo(0, {});".format(current_height + delta))
        current_height += delta
        time.sleep(0.1)
        page_height = page.evaluate("() => document.body.scrollHeight;")
        if current_height > page_height:
            break


def process_xlsx(page: Page, session: Session, vo: XlsxRequestVO):
    print("processing xlsx request: food_name={} start_date={}".format(vo.food_name,
                                                                       vo.start_date))
    # browser = p.chromium.launch(headless=app_config.headless)
    # page = browser.new_page()
    page.goto("https://eda.yandex.ru/moscow?shippingType=delivery")
    print("goto result={}".format(page.url))
    xlsx_request_repository.set_what_is_doing(session, vo, "Заходим на страницу")

    if page.url.split("/")[3].startswith("showcaptcha"):
        print("captcha page. solving...")
        xlsx_request_repository.set_what_is_doing(session, vo, "Решаем каптчу")
        solve_captcha.run(page)

    xlsx_request_repository.set_what_is_doing(session, vo, "Выставляем геолокацию на Москву")
    set_location(page)

    xlsx_request_repository.set_what_is_doing(session, vo, "Вбиваем поисковый запрос")
    search(page, vo.food_name)

    print("parsing shops")
    parse_all_shops(page, session, vo)

    xlsx_request_repository.set_what_is_doing(session, vo, "Формируем excel отчет")

    food_list = food_repository.get_all(session, vo.id)
    restaurant_list = restaurant_repository.find_all(session, vo.id)
    filename = "{}.xlsx".format(str(time.time()))
    path = "./reports/{}".format(filename)
    xlsx_service.to_csv(restaurant_list, food_list, path)

    vo.status = XlsxRequestStatus.completed
    vo.filename = filename
    vo.end_date = datetime.now()
    xlsx_request_repository.update(session, vo)
    xlsx_request_repository.set_what_is_doing(session, vo, "Завершено")

    restaurant_repository.delete_by_xlsx_request_id(session, vo.id)
    food_repository.delete_by_xlsx_request_id(session, vo.id)
    print("completed")


def main():
    with ThreadPoolExecutor(max_workers=app_config.max_workers) as executor:
        database.base.metadata.create_all(bind=database.engine)
        session = database.session_local()

        while True:
            xs = xlsx_request_repository.find_not_started(session)
            if len(xs) != 0:
                print("found {} requests".format(len(xs)))
            for xlsx_request_vo in xs:
                xlsx_request_vo.status = XlsxRequestStatus.started
                xlsx_request_repository.update(session, xlsx_request_vo)

                executor.submit(process_xlsx_task, xlsx_request_vo)
            time.sleep(1)


def process_xlsx_task(xlsx_request_vo: XlsxRequestVO):
    session = database.session_local()
    with sync_playwright() as p:
        try:
            page = p.chromium.launch(headless=app_config.headless).new_page()
            process_xlsx(page, session, xlsx_request_vo)
        except Exception as e:
            print(str(e))
            screenshot_util.screenshot(page, "FAIL")
            xlsx_request_vo.status = XlsxRequestStatus.failed
            xlsx_request_repository.update(session, xlsx_request_vo)


def test_run():
    database.base.metadata.create_all(bind=database.engine)
    session = database.session_local()
    vo = XlsxRequestVO(food_name="тоблерон")
    session.add(vo)
    session.commit()
    with sync_playwright() as p:
        page = p.chromium.launch(headless=app_config.headless).new_page()
        process_xlsx(page, session, vo)


def test_xlsx():
    database.base.metadata.create_all(bind=database.engine)
    session = database.session_local()

    food_list = food_repository.get_all(session)
    restaurant_list = restaurant_repository.find_all(session)
    filename = "{}.xlsx".format(str(time.time()))
    path = "./reports/{}".format(filename)
    xlsx_service.to_csv(restaurant_list, food_list, path)


if __name__ == "__main__":
    # test_xlsx()
    # test_run()
    main()
