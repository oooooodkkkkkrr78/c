from django.core.management import BaseCommand
import datetime
import os
import time
from django.core.files.base import File
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from telegram_bot_backend.settings import DRIVER_PATH
from latest_user_agents import get_random_user_agent
from Screenshot import Screenshot
from logger.views import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pickle

from tradingview.models import LoginCookie
from tradingview.tasks import absoluteSub

headers = {
    'user-agent': get_random_user_agent(),
}


def download_cookie():
    login_detailed_object = LoginCookie.objects.all()[0]
    logger('download snapshot has been started', 'd')
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    try:
        driver.get('https://www.tradingview.com/#signin')
        logger('https://www.tradingview.com/#signin', 'd')
        time.sleep(10)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        time.sleep(10)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(
            "dj1372")
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys("Amir#$1372" + Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(., 'Sign in')]]"))).click()

        print("login has been finished successfully")
        time.sleep(10)
        now_time = datetime.datetime.now()
        now_time = now_time.strftime('%d_%m_%Y')
        file_name = "trading_view_cookie" + "_" + now_time + '.pkl'
        pickle.dump(driver.get_cookies(), open(file_name, "wb"))

        with open(file_name) as f:
            login_detailed_object.file = File(f)
            login_detailed_object.save()
            time.sleep(1)
        os.remove(file_name)
        time.sleep(10)
        driver.quit()

    except Exception as e:
        logger('download cookie main exception' + str(e), 'd')


class Command(BaseCommand):
    def handle(self, *args, **options):
        from tradingview.tasks import absoluteSub
        result = absoluteSub.delay(10, 20)
        result.status
        result.get()



