
# Product by Rescue Alpha
#
# Discord:
# https://discord.gg/438gwCx5hw
#
# Telegram:
# https://t.me/rescue_alpha

import json
import os
import time

import zipfile
import pyperclip
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait

data = []
with open('data.txt', 'r') as file:
    for i in file:
        data.append(i.strip('\n'))

api_key = data[0]
link_ip = data[1]

def using_proxy():

    def get_proxy():
        proxy = {}

        with open("proxy.txt", "r") as file:
            proxy = file.readline()
            file.close()

        return proxy


    proxy = str(get_proxy())
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

    return manifest_json, background_js, proxy

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

    manifest_json, background_js, proxy = using_proxy()

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

    driver = webdriver.Chrome(ChromeDriverManager().install(),  options=chrome_options)

    return driver, proxy


def nft():

    driver, proxy = get_chromedriver(use_proxy=True, user_agent=True)

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

    time.sleep(5)

    # Регистрируем кошелек

    driver.get('chrome-extension://dlcobpjiigpikoobohmabehhmhfoodbb/index.html')

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[3]/button[1]')))
    ActionChains(driver).move_to_element(
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[3]/button[1]')).click().perform()

    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'label.MuiFormControlLabel-labelPlacementEnd')))
    labels = driver.find_elements(By.CSS_SELECTOR, 'label.MuiFormControlLabel-labelPlacementEnd')
    for label in labels:
        ActionChains(driver).move_to_element(label).click().pause(0.5).perform()

    time.sleep(2)

    ActionChains(driver).move_to_element(
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[3]/button')).click().perform()

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('Password123123')
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, 'input[name="repeatPassword"]').send_keys('Password123123')
    time.sleep(1)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()

    time.sleep(2)

    driver.switch_to.new_window()
    driver.get('chrome-extension://dlcobpjiigpikoobohmabehhmhfoodbb/index.html')

    # wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[2]/div/button[2]')))
    # driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/div/button').click()

    # time.sleep(10000)

    # wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/button')))
    # time.sleep(1)
    # ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/button')).click().perform()

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/div/button')))
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/div/button').click()

    address = pyperclip.paste()

    time.sleep(1)

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[role="alert"]')).click().perform()
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass

    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/recovery/seed?returnTo=%2Faccount%2Ftokens"]')))
    time.sleep(1)
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass
    ActionChains(driver).move_to_element(
        driver.find_element(By.CSS_SELECTOR, 'a[href="/recovery/seed?returnTo=%2Faccount%2Ftokens"]')).click().perform()

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass

    wait.until(visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/form/div[3]/button')))
    time.sleep(2)
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass
    ActionChains(driver).move_to_element(
        driver.find_element(By.XPATH,
                            '//*[@id="root"]/div/div/div[2]/div/form/div[3]/button')).click().perform()

    mnemonic = pyperclip.paste()

    time.sleep(2)

    ActionChains(driver).move_to_element(
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()

    time.sleep(2)

    try:
        ActionChains(driver).move_to_element(
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()
    except:
        pass

    time.sleep(2)

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="I understand"]')).click().perform()
    except:
        pass

    time.sleep(2)

    try:
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                                 '//button[text()="Reject"]')).click().perform()
    except:
        pass



    print(address, mnemonic)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # Запрашиваем токены в кране
    driver.get('https://faucet.goerli.starknet.io/')

    count = 0

    dd = True
    FF = True
    while FF == True:

        if dd == False:
            break

        wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(address)

        Wait(driver, 180).until(visibility_of_element_located((By.CSS_SELECTOR, '.antigate_solver.solved')))
        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[class*="Button_button_"]')).click().perform()

        tokens = 'Не получены'

        # while True:
        #     elements = driver.find_elements(By.CSS_SELECTOR, 'button[class*="Button_button_"]')
        #     if len(elements) == 2:
        #         break

        # ActionChains(driver).move_to_element(driver.find_elements(By.CSS_SELECTOR, 'button[class*="Button_button_"]')[1]).click().perform()

        while True:
            try:
                if driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[1]/div').text == 'Request complete':

                    tokens = 'Получены'

                    FF = False
                    break
                elif driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[1]/div').text == 'Request error':

                    if count == 2:
                        dd = False

                    driver.refresh()

                    count += 1

                    break


            except:
                pass

    print(tokens)



    time.sleep(2)

    with open("result.txt", "a+", encoding='utf-8') as file:
        file.writelines(f"{tokens}:::{proxy[:-1]}:::{address}:::{mnemonic}\n")

    # with open('proxy.txt', 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    #
    # with open('proxy.txt', 'w', encoding='utf-8') as file:
    #     lines = file.writelines(lines[1:])

    driver.quit()

    time.sleep(2)

    requests.get(link_ip)
    time.sleep(5)


def main():
    count = 0
    while True:
        try:

            nft()
            count = 0
        except Exception as e:

            if count >= 5:
                break

            # time.sleep(10000)
            print(e)
            count+=1


if __name__ == '__main__':



    main()
