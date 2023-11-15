


# Product by Rescue Alpha
#
# Discord:
# https://discord.gg/6Y4bvGsXuX
#
# Telegram:
# https://t.me/rescue_alpha



import json
import os
import random
import time

import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait

with open('data.txt', 'r') as file:
    api_key = file.readline()
    file.close()

names = []
with open('names.txt', 'r') as file:
    for i in file:
        names.append(i.strip('\n'))

def using_proxy():


    with open("result.txt", "r") as file:
        data = file.readline()
        file.close()

    proxy = str(data.split(':::')[1])
    mnemonic = str(data.split(':::')[-1])
    # print(data.split(':::')[-1])

    proxy_list = proxy.split(':')
    pass1 = str(proxy_list[3])

    PROXY_HOST = str(proxy_list[0])  # rotating proxy or host
    PROXY_PORT = str(proxy_list[1])
    PROXY_USER = str(proxy_list[2])
    PROXY_PASS = str(pass1.strip())

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "browsingData",
            "proxy",
            "storage",
            "tabs",
            "webRequest",
            "webRequestBlocking",
            "downloads",
            "notifications",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    return manifest_json, background_js, proxy, data.split(':::')


def acp_api_send_request(driver, message_type, data={}):
    message = {
        # всегда указывается именно этот получатель API сообщения
        'receiver': 'antiCaptchaPlugin',
        # тип запроса, например setOptions
        'type': message_type,
        # мерджим с дополнительными данными
        **data
    }
    # выполняем JS код на странице
    # а именно отправляем сообщение стандартным методом window.postMessage
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


def get_chromedriver(use_proxy=True, user_agent=UserAgent):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()

    manifest_json, background_js, proxy, data = using_proxy()

    if use_proxy:
        pluginfile = 'Proxy_ext.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)

    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)

    proxy_list = proxy.split(':')

    PROXY_HOST = str(proxy_list[0])  # rotating proxy or host
    PROXY_PORT = str(proxy_list[1])
    PROXY_USER = str(proxy_list[2])
    PROXY_PASS = str(proxy_list[3])

    chrome_options.add_extension('AntiCaptcha.zip')
    chrome_options.add_extension('ArgentX.crx')

    # selenium_wire_storage = os.path.join(
    #     os.getcwd(), "seleniumwire")

    # options = {'proxy': {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'},
    #            'request_storage_base_dir': selenium_wire_storage}

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    return driver, proxy, data


def nft():

    global proxy, mnemonic, address, progress

    driver, proxy, data = get_chromedriver(use_proxy=True, user_agent=True)

    mnemonic = data[-1]
    address = data[2]

    print(mnemonic)

    with open("mail.txt", "r") as file:
        mail = file.readline()
        file.close()

    with open("twitter.txt", "r") as file:
        twitter = file.readline()
        file.close()


    opts = Options()
    # print(driver.window_handles)
    wait = WebDriverWait(driver, 500)

    time.sleep(5)

    driver.maximize_window()

    while len(driver.window_handles) != 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()

    driver.switch_to.window(driver.window_handles[0])

    # Активируем антикапчу
    driver.get('https://antcpt.com/blank.html')
    acp_api_send_request(
        driver,
        'setOptions',
        {'options': {'antiCaptchaApiKey': api_key}}
    )

    # driver.get('https://www.google.com/')

    time.sleep(5)

    progress = 'Процесс не был выполнен'



    # Импортируем кошелек

    driver.get('chrome-extension://dlcobpjiigpikoobohmabehhmhfoodbb/index.html')

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[3]/button[2]')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[3]/button[2]')).click().perform()

    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
    time.sleep(2)

    for word in mnemonic.split(' '):
        ActionChains(driver).send_keys(word).perform()
        time.sleep(0.1)
        ActionChains(driver).send_keys(Keys.TAB).perform()

    time.sleep(1)
    ActionChains(driver).send_keys(Keys.SPACE).perform()

    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys('Password123123')
    ActionChains(driver).send_keys(Keys.TAB).pause(0.5).send_keys('Password123123').pause(0.5).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()

    wait.until(visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/a[1]')))

    driver.get('chrome-extension://dlcobpjiigpikoobohmabehhmhfoodbb/index.html')

    time.sleep(4)

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Create new wallet"]')).click().perform()

    except:
        pass

    time.sleep(5)

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass

    # wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div[3]/div/button')))
    # ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[3]/div/button')).click().perform()

    wait.until(visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/div/button')))

    driver.switch_to.new_window()
    driver.get('chrome-extension://dlcobpjiigpikoobohmabehhmhfoodbb/index.html')

    time.sleep(2)

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass

    driver.switch_to.window(driver.window_handles[0])

    progress = ''

    try:

        # Игра GOL2
        driver.get('https://goerli.gol2.io/infinite')

        wait.until(
            element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/header/header/div[2]/div/span/button/button')))
        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '/html/body/div[2]/div/header/header/div[2]/div/span/button/button')).click().perform()

        wait.until(element_to_be_clickable(
            (By.XPATH, '//*[@id="radix-:r1:"]/div[1]/button')))
        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//*[@id="radix-:r1:"]/div[1]/button')).click().perform()

        driver.switch_to.window(driver.window_handles[-1])
        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR,
                                                                     'circle[cx="16"]')).click().perform()
        except:
            pass

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()

        time.sleep(2)

        # try:
        #     ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/button')).click().perform()
        # except:
        #     pass

        try:
            ActionChains(driver).move_to_element(
                driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Close"]')).click().perform()
            time.sleep(1)
        except:
            pass

        driver.switch_to.window(driver.window_handles[0])

        wait.until(element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/div/header/span/button/button')))
        time.sleep(2)
        ActionChains(driver).move_to_element(
            driver.find_element(By.XPATH,
                                '/html/body/div[2]/div/div/div/div/div[1]/div/header/span/button/button')).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR,
                                                                     'circle[cx="16"]')).click().perform()
        except:
            pass

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()

        time.sleep(20)

        Wait(driver, 6000).until_not(
            visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Pending transactions"]')))

        driver.switch_to.window(driver.window_handles[0])

        time.sleep(3)

        ActionChains(driver).move_to_element(
            driver.find_elements(By.CSS_SELECTOR, 'path[stroke-linecap="round"]')[2]).click().perform()

        time.sleep(3)

        cubes = driver.find_elements(By.CSS_SELECTOR,
                                     'div[class*="remix-css-"] > div[class*="remix-css-"]> div[class*="remix-css-"]> div[class*="remix-css-"]> div[class*="remix-css-"]>div[class*="remix-css-"] > div[class*="remix-css-"] > div[class*="remix-css-"]')

        while True:

            try:
                ActionChains(driver).move_to_element(cubes[random.randint(0, 220)]).click().perform()
                break
            except:
                pass

        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '/html/body/div[2]/div/div/div/div/div[1]/div/div[1]/div/div/button[1]')).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR,
                                                                     'circle[cx="16"]')).click().perform()
        except:
            pass

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()

        time.sleep(20)

        Wait(driver, 6000).until_not(
            visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Pending transactions"]')))

        progress += ' GOL2 готово'

    except:
        pass

    driver.switch_to.window(driver.window_handles[0])

    # Заполняем форму

    driver.get('https://zkx.fi/404')

    try:
        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[class*="UiButton_wrap"]')))
        ActionChains(driver).move_to_element(
            driver.find_elements(By.CSS_SELECTOR, 'button[class*="UiButton_wrap"]')[0]).click().perform()

        wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'input[name="name"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name="name"]').send_keys(random.choice(names))

        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(mail)

        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, 'input[name="telegramIDTwitterID"]').send_keys(twitter)

        time.sleep(1)

        ActionChains(driver).send_keys(Keys.TAB).pause(1).send_keys(
            random.choice(['Germany', 'United States of America', 'France'])).pause(0.5).send_keys(Keys.ENTER).perform()
        time.sleep(1)

        ActionChains(driver).send_keys(Keys.TAB).pause(1).send_keys(
            random.choice(['Daily', 'Weekly', 'Monthly'])).pause(0.5).send_keys(Keys.ENTER).perform()
        time.sleep(1)

        ActionChains(driver).send_keys(Keys.TAB).pause(1).send_keys(
            random.choice(['Yes', 'No'])).pause(0.5).send_keys(Keys.ENTER).perform()
        time.sleep(1)

        ActionChains(driver).send_keys(Keys.TAB).pause(1).send_keys(
            random.choice(['From friends', 'From internet', 'Telegram', 'Twitter', 'Social media'])).pause(
            0.5).send_keys(Keys.ENTER).perform()

        Wait(driver, 180).until(visibility_of_element_located((By.CSS_SELECTOR, '.antigate_solver.solved')))

        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//*[@id="__next"]/div[2]/table/tbody/tr/td/div/div[2]/div[4]/div/button')).click().perform()

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])

        progress += ' + Форма отправлена'

    except:
        driver.switch_to.window(driver.window_handles[0])

    try:

        driver.get(
            f'https://mintsquare.io/asset/starknet-testnet/0x07b6d00f28db723199bb54ca74a879a5102c44141f0e93674b2cb25f8f253c62/{random.randint(1, 4000)}')

        time.sleep(5)

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'div[color="transparent"]')))
        ActionChains(driver).move_to_element(
            driver.find_elements(By.CSS_SELECTOR, 'div[color="transparent"]')[2]).click().perform()

        wait.until(visibility_of_element_located((By.XPATH, '//button[text()=" Connect Wallet"]')))
        time.sleep(3)

        ActionChains(driver).move_to_element(
            driver.find_element(By.XPATH, '//button[text()=" Connect Wallet"]')).click().perform()
        wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'img[alt="Argent X logo"]')))
        time.sleep(1)

        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'img[alt="Argent X logo"]')).click().perform()

        driver.switch_to.window(driver.window_handles[-1])
        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR,
                                                                     'circle[cx="16"]')).click().perform()
        except:
            pass

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()

        driver.switch_to.window(driver.window_handles[0])

        wait.until(element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div')).click().perform()

        wait.until(element_to_be_clickable((By.XPATH, '//button[text()=" Make Offer"]')))
        time.sleep(2)

        ActionChains(driver).move_to_element(
            driver.find_element(By.XPATH, '//button[text()=" Make Offer"]')).click().perform()

        wait.until(visibility_of_element_located((By.XPATH, '//span[text()="Customize end time"]')))
        time.sleep(2)

        ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys('0.0001').perform()
        time.sleep(1)

        ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
        time.sleep(3)

        ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[-1])
        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR,
                                                                     'circle[cx="16"]')).click().perform()
        except:
            pass

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()

        time.sleep(20)

        Wait(driver, 6000).until_not(
            visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Pending transactions"]')))

        driver.switch_to.window(driver.window_handles[0])

        try:
            driver.switch_to.window(driver.window_handles[-1])
            try:
                ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR,
                                                                         'circle[cx="16"]')).click().perform()
            except:
                pass

            wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            ActionChains(driver).move_to_element(
                driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()
        except:
            pass

        driver.switch_to.window(driver.window_handles[0])

        wait.until(element_to_be_clickable((By.XPATH, '//button[text()="Close this window"]')))
        ActionChains(driver).move_to_element(
            driver.find_element(By.XPATH, '//button[text()="Close this window"]')).click().perform()

        progress += ' + Сделан оффер на Mintsquare'

    except:
        driver.switch_to.window(driver.window_handles[0])

    driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)

    with open("abuse_result.txt", "a+") as file:
        file.write(f"{progress}:::{proxy}:::{address}:::{mnemonic[:-1]}:::{mail[:-1]}\n")

    with open('mail.txt', 'r') as file:
        lines = file.readlines()

    with open('mail.txt', 'w') as file:
        lines = file.writelines(lines[1:])

    with open('twitter.txt', 'r') as file:
        lines = file.readlines()

    with open('twitter.txt', 'w') as file:
        lines = file.writelines(lines[1:])

    with open('result.txt', 'r') as file:
        lines = file.readlines()

    with open('result.txt', 'w') as file:
        lines = file.writelines(lines[1:])

    print('Ready')
    # time.sleep(10000)

    driver.quit()


def main():
    while True:
        try:
            nft()

        except IndexError:
            break

        except Exception as e:

            with open("abuse_result.txt", "a+") as file:
                file.write(f"{progress}:::{proxy}:::{address}:::{mnemonic}")


            # time.sleep(10000)
            print(e)
            pass


if __name__ == '__main__':


    main()
