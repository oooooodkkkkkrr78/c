import threading

from PIL import Image
from tradingview.models import Watermark
from tradingview.tg_thread import TelegramThread
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram_bot_backend.settings import DRIVER_PATH
from latest_user_agents import get_random_user_agent
from logger.views import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tradingview.models import LoginCookie
import pickle

headers = {
    'user-agent': get_random_user_agent(),
}


def sendAlert(context):
    logger(str(context), 'd')
    data = context['data']
    logger(str(data), 'd')
    print(str(data))
    msg = ""

    try:
        msg = data["msg"]
        msg = msg.encode("latin-1", "backslashreplace") \
            .decode("unicode_escape")
    except Exception as e:
        logger(str(e), 'd')
        msg = ""
    logger(str(msg), 'd')
    tf = data["tf"].upper()
    logger(str(tf), 'd')
    sgFa = getStrategy(data["sg"], 'fa')
    logger(str(sgFa), 'd')
    sgEn = getStrategy(data["sg"], 'en')
    try:
        chart_id = data["ch"]
    except Exception as e:
        logger("chart id" + str(e), 'd')
        chart_id = "-"
    logger(str(chart_id), 'd')
    zoom = data["zm"]
    logger(str(zoom), 'd')

    symbols = getSymbol(data["sy"])
    logger(str(symbols), 'd')

    exchangers = []
    for s in symbols:
        exchangers.append(getExchange(s))
    logger(str(exchangers), 'd')
    timeframe = tf

    SnapMainThread(trading_view_url(exchangers, chart_id, symbols, tf), symbols, exchangers, timeframe, sgFa, msg, "fa",
                   context['channels'], context['sign'], chart_id,
                   context['has_image'], context['has_watermark'], zoom).start()
    time.sleep(5)
    logger('SnapMainThread has been started. symbols: ' + str(symbols) + " exchange: " + str(exchangers), 'd')


class SnapMainThread(threading.Thread):
    def __init__(self, trading_view_urls, symbols, exchangers, timeframe, strategy, message, lang, channels, sign,
                 chart_id,
                 context_has_image, context_has_watermark, zoom):
        threading.Thread.__init__(self)
        self.symbols = symbols
        self.exchangers = exchangers
        self.timeframe = timeframe
        self.strategy = strategy
        self.message = message
        self.lang = lang
        self.channels = channels
        self.sign = sign
        self.chart_id = chart_id
        self.context_has_image = context_has_image
        self.context_has_watermark = context_has_watermark
        self.zoom = zoom
        self.trading_view_urls = trading_view_urls

    def run(self):
        tries = 0
        while True:
            try:
                sending_data_to_channel = {
                    'symbols': self.symbols,
                    'exchangers': self.exchangers,
                    'timeframe': self.timeframe,
                    'strategy': self.strategy,
                    'message': self.message,
                    "lang": self.lang,
                    'channels': self.channels,
                    'sign': self.sign,
                    'chart_id': self.chart_id,
                }

                if self.context_has_image == 0:
                    logger(str(self.context_has_image) + ": 0", 'd')
                    sending_data_to_channel['image'] = ''
                    TelegramThread(telegram_message_creator(sending_data_to_channel), self.channels).start()
                else:
                    logger(str(self.context_has_image) + ": not 0", 'd')
                    download_snapshot(self.trading_view_urls,
                                      self.context_has_watermark,
                                      self.zoom,
                                      sending_data_to_channel,
                                      )
                return logger('snap download has been succeeded. symbol: ' + str(self.symbols) + " exchanger: " + str(
                    self.exchangers), 'd')
            except Exception as e:
                logger('snap thread exception has happened. err: ' + str(e) + " number of tries: " + str(), 'd')
                tries += 1
                if tries == 3:
                    return logger('snap download has been failed. symbol: ' + str(self.symbols) + " exchanger: " + str(
                        self.exchangers) + " number of tries: " + str(tries), 'd')


def telegram_message_creator(sending_data):
    logger('start telegram message creator', 'd')
    if sending_data['sign'] == 1:
        sign = '👉'
    elif sending_data['sign'] == 2:
        sign = '👈'
    else:
        sign = ''
    logger('sign: ' + str(sign), 'd')
    symb = str(getSymbolName(sending_data['symbol'], sending_data['lang']))
    symb = symb.replace(' ', '')
    symb = symb.replace('/', '')
    symb = symb.replace('(', '')
    symb = symb.replace(')', '')
    message = "<a href='" + sending_data['image'] + "'>▫️</a>" + \
              sign + " " + sending_data['strategy'] + "\n\n" + \
              "📊 " + "[ " + symb + " / " + getTimeFrame(sending_data['timeframe'], 'en') + " ]" + "\n\n" + \
              "My id " + "<tg-spoiler><a href='" + "https://google.com" + "'>" + "info" + "</a></tg-spoiler>" + "\n\n"
              # "<b>پیام: </b>" + sending_data['message'] + "\n\n" + \
              # "<b>جفت ارز: </b>" + getSymbolName(sending_data['symbol'], sending_data['lang']) + "\n\n" + \
              # "<b>تایم فریم: </b>" + getTimeFrame(sending_data['timeframe'], sending_data['lang']) + "\n\n" + \
              # "<b>استراتژی: </b>" + sending_data['strategy'] + "\n\n" + \
              # "<b>پیام: </b>" + sending_data['message'] + "\n\n" + \
              # sign + "\n\n" + \
              # "<tg-spoiler><a href='" + "https://google.com" + "'>" + "سلام" + "</a></tg-spoiler>" + "\n"
    logger('message: ' + message, 'd')
    return message
    # elif sending_data['lang'] == 'en':
    #     message = "<a href='" + sending_data['image'] + "'>▫️</a>" + \
    #               "<b>Pair: </b>" + getSymbolName(sending_data['symbol'], sending_data['lang']) + "\n\n" + \
    #               "<b>Timeframe: </b>" + getTimeFrame(sending_data['timeframe'], sending_data['lang']) + "\n\n" + \
    #               "<b>Strategy: </b>" + sending_data['strategy'] + "\n\n" + \
    #               "<b>Message: </b>" + sending_data['message'] + "\n\n" + \
    #               sign + "\n\n" + \
    #               "<tg-spoiler><a href='" + "https://google.com" + "'>" + "Salam" + "</a></tg-spoiler>" + "\n"
    #     logger('message: ' + message, 'd')
    #     return message


def getTimeFrame(tf, lang):
    u = tf[-1]
    d = tf[0:-1]

    if u == 'S':
        return {
            'fa': d + " ثانیه",
            'en': d + " Second",
        }[lang]
    elif u == 'H':
        return {
            'fa': d + " ساعته",
            'en': d + " Hour",
        }[lang]
    elif u == 'D':
        return {
            'fa': d + " روزه",
            'en': d + " Day",
        }[lang]
    elif u == 'W':
        return {
            'fa': d + " هفته",
            'en': d + " Week",
        }[lang]
    elif u == 'M':
        return {
            'fa': d + " ماهه",
            'en': d + " Month",
        }[lang]
    elif u == 'Y':
        return {
            'fa': d + " ساله",
            'en': d + " Year",
        }[lang]
    else:
        return {
            'fa': tf + " دقیقه",
            'en': tf + " Minute",
        }[lang]


def getExchange(sy):
    m = sy[-4:]
    if m != "USDT":
        return "FOREXCOM".upper()
    return "BINANCE".upper()


candleCode = {
    10: 50,
    11: 65,
    12: 80,
    13: 95,
    14: 110,
    15: 125,
    16: 140,
    17: 155,
    18: 170,
    19: 185,
    20: 200,
    21: 215,
    22: 230,
    23: 245,
    24: 260,
    25: 275,
    26: 290,
    27: 305,
    28: 320,
    29: 335,
    30: 350,
    31: 365,
    32: 380,
    33: 395,
    34: 410,
    35: 425,
    36: 440,
    37: 455,
    38: 470,
    39: 485,
    40: 500,
}


def getCandles(cl):
    try:
        cl = str(cl)
        codes = []
        l = len(cl)
        if l % 2 != 0:
            return cl
        for x in range(int(l / 2)):
            codes.append(candleCode[int(cl[2 * x:2 * x + 2])])
        return codes
    except:
        return cl


def getStrategy(sg, lang):
    try:
        code = int(sg[-1])
        name = sg[0:-1]
        if lang == 'en':
            if name == "SRF":
                if code == 1:
                    return " 🟢"
                if code == 2:
                    return "P 🔴"
            if name == "DIV":
                if code == 1:
                    return "Bulli 🟢"
                if code == 2:
                    return "B 🔴"
                if code == 3:
                    return "B 🟢"
                if code == 4:
                    return ""
            if name == "FIB":
                if code == 1:
                    return ""
                if code == 2:
                    return "P"
            if name == "SHE":
                if code == 1:
                    return " 🟢"
                if code == 2:
                    return "🔴"
            if name == "PUL":
                if code == 1:
                    return "P 🟢"
                if code == 2:
                    return " 🔴"
            if name == "CHA":
                if code == 1:
                    return "P 🟢"
                if code == 2:
                    return "P🔴"
        else:
            if name == "SRF":
                if code == 1:
                    return "  🟢"
                if code == 2:
                    return " 🔴"
            if name == "DIV":
                if code == 1:
                    return " 🟢"
                if code == 2:
                    return " 🔴"
                if code == 3:
                    return " 🟢"
                if code == 4:
                    return " 🔴"
            if name == "FIB":
                if code == 1:
                    return " در "
                if code == 2:
                    return ""
            if name == "SHE":
                if code == 1:
                    return "شت 🟢"
                if code == 2:
                    return " 🔴"
            if name == "PUL":
                if code == 1:
                    return "پوه 🟢"
                if code == 2:
                    return "پو 🔴"
            if name == "CHA":
                if code == 1:
                    return "  🟢"
                if code == 2:
                    return "  🔴"

        return sg
    except:
        return sg


symbolCode = {
    10: 'BTCUSDT',
    11: 'ETHUSDT',
    12: 'BNBUSDT',
    13: 'XRPUSDT',
    14: 'SHIBUSDT',
    15: 'ADAUSDT',
    16: 'EURUSD',
    17: 'USDJP',
    18: 'XAUUSD',
    19: 'ATOMUSDT',
    20: 'MATICUSDT',
    21: 'SOLUSDT',
    22: 'LTCUSDT',
    23: 'TRXUSDT',
    24: 'DOGEUSDT',
    25: 'LINKUSDT',
    26: 'NEARUSDT',
    27: 'AVAXUSDT',
    28: 'DOTUSDT',
    29: 'USDCAD',
    30: 'NZDUSD',
    31: 'AUDUSD',
    32: 'GBPUSD',
    33: 'USDCHF',
}


def getSymbol(sy):
    if type(sy) == int or type(sy) == str and sy.isnumeric():
        sy = str(sy)
        codes = []
        l = len(sy)
        if l % 2 != 0:
            return False
        try:
            for x in range(int(l / 2)):
                codes.append(symbolCode[int(sy[2 * x:2 * x + 2])].upper())
        except:
            return False
        return codes
    elif type(sy) == str:
        return sy.upper()
    return "BTCUSDT".upper()


persianSymbols = {
    "BTCUSDT": " (BTCUSDT)",
    "ETHUSDT": " /  (ETHUSDT)",
    "BNBUSDT": "‌  /  (BNBUSDT)",
    "XRPUSDT": " /  (XRPUSDT)",
    "SHIBUSDT": " /  (SHIBUSDT)",
    "ADAUSDT": " /  (ADAUSDT)",
    "EURUSD": "   /  (EURUSD)",
    "USDJPY": "  /   (USDJPY)",
    "XAUUSD": "  /  (XAUUSD)",
}

englishSymbols = {

}


def getSymbolName(sy, lang):
    if lang == 'fa':
        try:
            return persianSymbols[sy]
        except:
            return sy
    else:
        try:
            return englishSymbols[sy]
        except:
            return sy


def download_snapshot(trading_view_urls, which_watermark, zoom, sending_data_to_channel):
    logger('download snapshot has been started', 'd')
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    try:
        driver.get('https://www.tradingview.com/')
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        i_list = [0, ]
        i = 0
        for url in trading_view_urls:
            dummy = str(url)
            dummy = dummy.replace('symbol=', ' ')
            dummy = dummy.replace(':', ' ')
            dummy = dummy.replace('&interval=', ' &interval=')
            dummy = dummy.split()
            symbol = dummy[3]
            print(symbol)
            sending_data_to_channel['symbol'] = symbol
            exchange = dummy[2]
            print(exchange)
            sending_data_to_channel['exchange'] = exchange
            logger(url, 'd')
            if i == 0:
                driver.get(url)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[6]/div/div/div/article/div/div/div/button[2]/span'))).click()

                action = ActionChains(driver)
                z = 0
                logger('zoom: ' + str(zoom), 'd')
                if int(zoom) < 0:
                    action.key_down(Keys.ALT).key_down('r').key_up(Keys.ALT).key_up('r').perform()
                    time.sleep(0.5)
                    while True:
                        action.key_down(Keys.CONTROL).key_down(Keys.ARROW_DOWN).key_up(Keys.CONTROL).key_up(
                            Keys.ARROW_DOWN).perform()
                        time.sleep(0.5)
                        z -= 1
                        print(int(zoom))
                        print(z)
                        if z == int(zoom):
                            break
                elif int(zoom) > 0:
                    action.key_down(Keys.ALT).key_down('r').key_up(Keys.ALT).key_up('r').perform()
                    time.sleep(0.5)
                    while True:
                        action.key_down(Keys.CONTROL).key_down(Keys.ARROW_UP).key_up(Keys.CONTROL).key_up(
                            Keys.ARROW_UP).perform()
                        time.sleep(0.5)
                        z += 1
                        if z == int(zoom):
                            break
                else:
                    pass
            else:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[i])
                driver.get(url)
                action = ActionChains(driver)
                z = 0
                logger('zoom: ' + str(zoom), 'd')
                if int(zoom) < 0:
                    action.key_down(Keys.ALT).key_down('r').key_up(Keys.ALT).key_up('r').perform()
                    time.sleep(0.5)
                    while True:
                        action.key_down(Keys.CONTROL).key_down(Keys.ARROW_DOWN).key_up(Keys.CONTROL).key_up(
                            Keys.ARROW_DOWN).perform()
                        time.sleep(0.5)
                        z -= 1
                        print(int(zoom))
                        print(z)
                        if z == int(zoom):
                            break
                elif int(zoom) > 0:
                    action.key_down(Keys.ALT).key_down('r').key_up(Keys.ALT).key_up('r').perform()
                    time.sleep(0.5)
                    while True:
                        action.key_down(Keys.CONTROL).key_down(Keys.ARROW_UP).key_up(Keys.CONTROL).key_up(
                            Keys.ARROW_UP).perform()
                        time.sleep(0.5)
                        z += 1
                        if z == int(zoom):
                            break
                else:
                    pass

            i += 1
            i_list.append(i)
            print(i_list)
        i = 0
        for url in trading_view_urls:
            driver.switch_to.window(driver.window_handles[i])
            time.sleep(0.5)
            dummy = str(url)
            dummy = dummy.replace('symbol=', ' ')
            dummy = dummy.replace(':', ' ')
            dummy = dummy.replace('&interval=', ' &interval=')
            dummy = dummy.split()
            symbol = dummy[3]
            print(symbol)
            sending_data_to_channel['symbol'] = symbol
            exchange = dummy[2]
            print(exchange)
            sending_data_to_channel['exchange'] = exchange
            logger(url, 'd')
            now_time = datetime.datetime.now()
            now_time = now_time.strftime('%d-%m-%Y-%H-%M-%S')
            filename = now_time + "-" + symbol + "-" + exchange + str(".png")
            logger(filename, 'd')
            image = driver.find_element(By.CLASS_NAME, 'layout__area--center').screenshot(
                os.path.join(os.path.join('media', 'snapshot'), filename))
            watermark = ''
            if which_watermark == 0:
                logger('no watermark has been picked', 'd')
                snapshot_file_address = os.path.join('media', 'snapshot/' + filename)
                snapshot_file_address = snapshot_file_address.replace('\\', "")
                sending_data_to_channel['symbol'] = symbol
                sending_data_to_channel['image'] = 'https://shabake-art.ir/' + str(snapshot_file_address)
                TelegramThread(telegram_message_creator(sending_data_to_channel),
                               sending_data_to_channel['channels']).start()
            else:
                if which_watermark == 1:
                    watermark = Watermark.objects.all().order_by('-id')[0]
                elif which_watermark == 2:
                    watermark = Watermark.objects.all().order_by('-id')[1]
                snapshot = Image.open(os.path.join('media', 'snapshot/' + filename))
                watermark = Image.open(watermark.watermark.path)
                snapshot = snapshot.convert("RGBA")
                watermark = watermark.convert("RGBA")
                width = (snapshot.width - watermark.width) // 2
                height = (snapshot.height - watermark.height) // 2
                snapshot.paste(watermark, (width, height), watermark)
                filename = 'watermarked' + "-" + str(filename)
                snapshot.save(os.path.join('media/snapshot_watermarked', filename), format="png")
                logger('watermarked image has been saved', 'd')
                watermarked_snapshot_file_address = os.path.join('media', 'snapshot_watermarked/' + filename)
                watermarked_snapshot_file_address = watermarked_snapshot_file_address.replace('\\', "")
                sending_data_to_channel['symbol'] = symbol
                sending_data_to_channel['image'] = 'https://shabake-art.ir/' + str(watermarked_snapshot_file_address)
                TelegramThread(telegram_message_creator(sending_data_to_channel),
                               sending_data_to_channel['channels']).start()
            i += 1
        driver.quit()
        time.sleep(120)
    except Exception as e:
        logger('download snapshot main exception. err: ' + str(e), 'd')


def download_cookie():
    logger('download cookie has been started', 'd')
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    try:
        login_detailed_object = LoginCookie.objects.all()[0]
        user_name = str(login_detailed_object.user_name)
        passwd = str(login_detailed_object.password)
        driver.get('https://www.tradingview.com/#signin')
        logger('https://www.tradingview.com/#signin', 'd')
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(
            user_name)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(passwd + Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(., 'Sign in')]]"))).click()

        print("login has been finished successfully")
        time.sleep(5)
        ccc = driver.get_cookies()
        print(ccc)
        login_detailed_object = LoginCookie.objects.all()[0]
        login_detailed_object.cookies = driver.get_cookies()
        login_detailed_object.save()
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        time.sleep(2)
        driver.quit()
        print('cookie download has finished')
    except Exception as e:
        logger('download cookie main exception' + str(e), 'd')


def trading_view_url(exchangers_name, chart_id, symbols_name, interval):
    url_list = []
    for symbol_name in symbols_name:
        url = 'https://www.tradingview.com/chart/' + chart_id + '/?symbol=' + exchangers_name[0] + ':' + symbol_name + '&interval=' + interval
        url_list.append(url)
    return url_list
