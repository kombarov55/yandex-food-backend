import json

from playwright.sync_api import Page


def copy_cookies(page: Page, path: str):
    cookies = page.context.cookies()
    with open(path, "w") as file:
        file.write(json.dumps(cookies))


def load_cookies(page: Page, path: str):
    with open(path) as file:
        s = file.read()
        cookies = json.loads(s)
        page.context.clear_cookies()
        page.context.add_cookies(cookies)
