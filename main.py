import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import await_user


class Liker:
    opensea_url = 'https://opensea.io'
    scroll_pixels = 100

    def __init__(self, executable_path, user_profile_path):
        self.executable_path = executable_path
        self.user_profile_path = user_profile_path
        self.driver = webdriver.Chrome(options=self.get_options(),
                                       executable_path=self.executable_path)

    def get_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--enable-file-cookies")
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f"--user-data-dir={self.user_profile_path}")
        return options

    def open_and_switch_new_tab(self, url):
        self.driver.execute_script(f"window.open('{url}')")
        self.driver.switch_to.window(self.driver.window_handles[1])

    def click_like(self):
        button = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.item--wrapper article header div:nth-child(3) button')))
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(1)

    def get_links_by_range(self, first, last):
        cards = WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                f'.AssetsSearchView--assets>div>div:nth-child(n+{first}):nth-child(-n+{last}) article a')))
        return [card.get_attribute('href') for card in cards]

    def close_and_return_to_first_page(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_opensea_page(self, path):
        liker.driver.get(f'{self.opensea_url}{path}')

    def scroll_page(self):
        print('Скроллим страницу')
        self.scroll_pixels += 407.39
        self.driver.execute_script(f"window.scrollTo(0, {self.scroll_pixels});")


if __name__ == '__main__':
    amount_likes = int(input('Введите количество лайков'))
    liker = Liker("/usr/local/bin/chromedriver", "/home/andrey/.config/google-chrome")

    time.sleep(1)
    liker.open_opensea_page('/login?referrer=%2Faccount')

    await_user(35)
    liker.open_opensea_page('/assets')

    amount_errors = 0
    handled_element = 0
    scrolls_pixels = 0

    while True:
        try:
            links = liker.get_links_by_range(handled_element + 1, handled_element + 5)
        except selenium.common.exceptions.TimeoutException:
            liker.open_opensea_page('/assets')
            continue

        for link in links:
            if not link:
                print('Непрогрузившаяся ссылка')
                time.sleep(10)
                continue
            liker.open_and_switch_new_tab(link)
            try:
                print(f'like №{handled_element}')
                liker.click_like()
            except Exception as err:
                amount_errors += 1
                print(err)
                print(f'Ошибка №{amount_errors} идем дальше')
            liker.close_and_return_to_first_page()
            handled_element += 1
        liker.scroll_page()
        time.sleep(2)
        if handled_element >= amount_likes:
            break
        continue
