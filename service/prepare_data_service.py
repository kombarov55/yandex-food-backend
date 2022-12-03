from threading import Thread

from playwright.sync_api import sync_playwright

import yandex_food_parser
from config import database
from repository import xlsx_request_repository


def run_background():
    session = database.session_local()
    should_load_data = xlsx_request_repository.should_load_data(session)
    print("should load data? {}".format(should_load_data))
    if should_load_data:
        Thread(target=load_data).start()


def load_data():
    session = database.session_local()
    vo = xlsx_request_repository.create(session, "Цезарь", True)

    with sync_playwright() as p:
        page = p.chromium.launch(headless=True).new_page()
        yandex_food_parser.parse_data_and_save_to_db(page, session, vo)
