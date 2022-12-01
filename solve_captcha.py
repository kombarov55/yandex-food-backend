import io
import time

import requests
from PIL import Image
from playwright.sync_api import Page, sync_playwright
from twocaptcha import TwoCaptcha


def run(page: Page):
    page.click("input.CheckboxCaptcha-Button")
    while True:
        page.wait_for_selector("img.AdvancedCaptcha-Image")
        print("clicked at yandex captcha button")

        print("downloading img..")
        src = page.locator("img.AdvancedCaptcha-Image").get_attribute("src")
        download_img(src)
        print("image downloaded")

        print("requesting captcha")
        text = request_solving()
        print("sending {}".format(text))

        page.locator("input.Textinput-Control").type(text, delay=100)
        print("typed {}".format(text))

        page.click("button.CaptchaButton")
        print("clicked at ОТПРАВИТЬ")

        time.sleep(3)

        if not page.url.split("/")[3].startswith("showcaptcha"):
            print("captcha solved")
            break
        print("solving another captcha")
    page.pause()


def download_img(src):
    content = requests.get(src).content
    image_file = io.BytesIO(content)
    image = Image.open(image_file)
    with open("captcha.png", "wb") as f:
        image.save(f, "png")


def request_solving():
    solver = TwoCaptcha("665080ecc6111b94809f7d4fbba65b29")
    result = solver.normal("captcha.png")
    print("received result: {}".format(result))
    return result["code"]


def scratch_run():
    with sync_playwright() as p:
        page = p.chromium.launch(headless=False).new_page()
        page.goto("https://eda.yandex.ru/showcaptcha?cc=1&mt=2222D2F3BAFCBB2868FA600DD8A04014A76A56B6EAFC893200545E209F266858E107&retpath=aHR0cHM6Ly9lZGEueWFuZGV4LnJ1L21vc2Nvdz9zaGlwcGluZ1R5cGU9ZGVsaXZlcnk%2C_fd0593559cbccee517013bb08a73d4e7&t=2/1669864357/e42cd551726da3cc57dd84cfbfd0b7e7&u=3fd44ba6-367ad839-49e24c60-d327ca0&s=c05c58683bb672c01eef1e6937bfe4e0")
        run(page)


if __name__ == "__main__":
    scratch_run()
