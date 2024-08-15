import threading
import time

import telegram

from logger.views import logger
from tradingview.models import TelegramSetting


class TelegramThread(threading.Thread):
    def __init__(self, message, channels_id):
        threading.Thread.__init__(self)
        self.message = message
        self.channels_id = channels_id

    def run(self):
        logger('start send to tg channel', 'd')
        i = 0
        for channel_id in self.channels_id:
            try:
                channel_details = TelegramSetting.objects.get(id=channel_id)
                bot = telegram.Bot(token=channel_details.bot_token)
                while True:
                    b = 0
                    try:
                        bot.send_message(chat_id=channel_details.channel_name,

                                         text=self.message,
                                         parse_mode=telegram.ParseMode.HTML)
                        break
                    except Exception as e:
                        b += 1
                        if b == 4:
                            break
                        logger('error has happened while sending message to channel: ' + str(e), 'd')
                        logger('waiting for 15 sec...', 'd')
                        time.sleep(15)

                logger('message has bees send successfully', 'd')
                i += 1
            except Exception as e:
                logger("TelegramThread exception. err: " + str(e), 'd')
        return logger('all messages has bees sends to channels successfully', 'd')
