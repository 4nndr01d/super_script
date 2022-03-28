import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://opensea.io/'


def get_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-data-dir=/home/andr01d/.config/google-chrome")
    return options


if __name__ == '__main__':
    amount_likes = int(input('Введите количество лайков'))
    # amount_likes = 100

    driver = webdriver.Chrome(options=get_options(),
                              executable_path="/usr/local/bin/chromedriver")
    driver.get(f'{url}login?referrer=%2Faccount')

    # todo Передать действие пользователю

    for i in range(30):
        time.sleep(1)
        if i % 10 == 0:
            print(f"Осталось {30 - i} сек...")

    print('Контроль возвращается боту')
    driver.get(f'{url}assets')
    amount_errors = 0
    liked_element = 1
    scroll_pixels = 6000
    while True:
        try:
            buttons = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[role=gridcell] article footer div:nth-child(2) button')))
        except selenium.common.exceptions.TimeoutException:
            driver.get(f'{url}assets')
            continue

        for button in buttons:
            try:
                print(f'like №{liked_element}')
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)
                liked_element += 1
            except:
                amount_errors += 1
                print(f'Ошибка №{amount_errors} идем дальше')
        driver.execute_script(f"window.scrollTo(0, {scroll_pixels});")
        scroll_pixels += 6000
        if liked_element >= amount_likes:
            break
