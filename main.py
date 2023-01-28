import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://opensea.io'


def get_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    # options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-data-dir=/home/andrey/.config/google-chrome")
    return options


def open_and_switch_new_tab(driver, url):
    driver.execute_script(f"window.open('{url}')")
    driver.switch_to.window(driver.window_handles[1])


def get_links(driver):
    cards = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(
        (By.CSS_SELECTOR, 'a.Asset--anchor')))
    return [card.get_attribute('href') for card in cards]


if __name__ == '__main__':
    # amount_likes = int(input('Введите количество лайков'))
    amount_likes = 35

    driver = webdriver.Chrome(options=get_options(),
                              executable_path="/usr/local/bin/chromedriver")

    time.sleep(1)
    driver.get(f'{url}/login?referrer=%2Faccount')

    for i in range(10):
        time.sleep(1)
        if i % 5 == 0:
            print(f"Осталось {10 - i} сек...")

    print('Контроль возвращается боту')
    driver.get(f'{url}/assets')
    amount_errors = 0
    handled_element = 1
    scroll_pixels = 6000
    while True:
        try:
            links = get_links(driver)
        except selenium.common.exceptions.TimeoutException:
            driver.get(f'{url}/assets')
            continue

        for link in links:
            open_and_switch_new_tab(driver, link)
            try:
                print(f'like №{handled_element}')
                button = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '.item--wrapper article header div:nth-child(3) button')))
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(0.5)
            except Exception as err:
                amount_errors += 1
                print(err)
                print(f'Ошибка №{amount_errors} идем дальше')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            handled_element += 1
        driver.execute_script(f"window.scrollTo(0, {scroll_pixels});")
        scroll_pixels += 6000
        if handled_element >= amount_likes:
            break
