from playwright.sync_api import Page

from config import app_config


def screenshot(page: Page, label: str):
    if app_config.screenshot_allowed:
        print(label)
        page.screenshot(path=app_config.screenshot_dir + "/" + label + ".png")
