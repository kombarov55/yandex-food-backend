import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from config import database
from model.food import FoodVO
from model.restaurant import RestaurantVO
from repository import restaurant_repository, food_repository

browser = webdriver.Chrome(r"C:\Users\komba\Documents\chromedriver.exe")
# browser.implicitly_wait(10000)

address = "Москва, Красная площадь 3"
food_name = "том-ям"

database.base.metadata.create_all(bind=database.engine)
session = database.session_local()

def set_location(location):
    select_location = browser.find_element(By.CSS_SELECTOR, "button.DesktopHeader_addressButton")
    select_location.click()

    address_input = browser.find_element(By.CSS_SELECTOR, "input.AppAddressInput_addressInput")
    browser.find_element(By.CSS_SELECTOR, "svg.AppAddressInput_closeIcon").click()
    address_input.send_keys(location)
    address_input.send_keys(Keys.ENTER)

    WebDriverWait(browser, 10).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button.DesktopLocationModal_ok")))
    browser.find_element(By.CSS_SELECTOR, "button.DesktopLocationModal_ok").click()
    WebDriverWait(browser, 10).until(
        expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "span.DesktopAddressButton_addressStreet"),
                                                          "Красная площадь"))


def find(search):
    browser.get("https://eda.yandex.ru/search?query={}&type=all".format(search))
    # wait_for_element_to_have_text("h1", "DesktopSearchPageContainer_pageHeader", "Найдено")
    WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[@class='DesktopSearchPageContainer_pageHeader' and contains(text(), 'Найдено')]")))
    # scroll_slowly_to_bottom()

    restaurants = browser.find_elements(By.CSS_SELECTOR, "div.DesktopSearchPlaceCarousel_info")

    list = [restaurants[1]]

    for restaurant in restaurants:
        scroll_to_element(restaurant)
        restaurant.click()
        browser.switch_to.window(browser.window_handles[1])
        parse_page()
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    # parse_page(titles[1])
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()


def parse_page():
    WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "li.RestaurantCategories_item")))

    restaurant_name = browser.find_element(By.CSS_SELECTOR, "h1.RestaurantHeader_name").text

    restaurant_vo = RestaurantVO(name=restaurant_name)
    restaurant_vo = restaurant_repository.save(session, restaurant_vo)

    menu_categories = browser.find_elements(By.CSS_SELECTOR, "li.RestaurantCategories_item")
    menu_categories[len(menu_categories) - 1].click()
    menu_categories[0].click()
    food_items = browser.find_elements(By.CSS_SELECTOR, "div.RestaurantMenu_item")
    print(len(food_items))

    # elements = [food_items[0], food_items[30]]

    for el in food_items:
        scroll_to_element(el)
        price = el.find_element(By.CSS_SELECTOR, "span.UiKitDesktopProductCard_price").text
        name = el.find_element(By.CSS_SELECTOR, "div.UiKitDesktopProductCard_name").text
        src = el.find_element(By.CSS_SELECTOR, "img.SmartImage_image").get_attribute("src")
        weight = el.find_element(By.CSS_SELECTOR, "div.UiKitDesktopProductCard_weight").text

        food_vo = FoodVO(restaurant_id=restaurant_vo.id, name=name, src=src, price=price, weight=weight)
        food_repository.save(session, food_vo)
        print("saved {}".format(food_vo.name))


def scroll_to_element(element: WebElement):
    ActionChains(browser).move_to_element(element).perform()


def scroll_slowly_to_bottom():
    current_height = 0
    delta = 500

    while True:
        browser.execute_script("window.scrollTo(0, {});".format(current_height + delta))
        current_height += delta
        time.sleep(0.1)
        page_height = browser.execute_script("return document.body.scrollHeight;")
        if current_height > page_height:
            break


def wait_for_element_to_have_text(tag, class_name, text):
    return WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//{}[@class='{}' and contains(text(), '{}')]".format(tag, class_name, text))))


def main():
    browser.get("https://eda.yandex.ru/moscow?shippingType=delivery")
    WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "(//h2[@class='DesktopHeaderBlock_headerText DesktopHeaderBlock_headerTextBold'])[1]")))

    set_location(address)
    find(food_name)


main()
