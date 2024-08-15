import json
import threading
import time
from django.http import HttpResponse

from tradingview.tg_thread import TelegramThread
from tradingview.utils import sendAlert, download_cookie
from tradingview.models import Key


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp


def cookie_reset_view(request, key):
    secure_keys = Key.objects.all()
    has_access = False
    for s_key in secure_keys:
        if s_key.secure_key == key:
            has_access = True
    if not has_access:
        return HttpResponse('Wrong key')
    Download_Cookie().start()
    return HttpResponse('Ok')


def webhook_view(request, key):
    context = {}
    if request.method == "POST":
        secure_keys = Key.objects.all()
        has_access = False
        for s_key in secure_keys:
            if s_key.secure_key == key:
                has_access = True
        if not has_access:
            return HttpResponse('Wrong key')

        input_json = request.body
        input_json = input_json.decode('utf8').replace("'", '"')
        data = json.loads(input_json)

        context['data'] = data

        try:
            channels = data['ch_ids']
            print(channels)
            if channels == '':
                return HttpResponse('Channels problem. Wrong choice')
            channels = str(channels).replace('_', ' ')
            channels = channels.split()
            context['channels'] = channels
        except Exception as e:
            return HttpResponse('Channels problem. err: ' + str(e))

        try:
            has_watermark = data['wt']
            if has_watermark == '':
                return HttpResponse('watermark problem. Wrong choice')
            if has_watermark == 0:
                context['has_watermark'] = 0
            elif has_watermark == 1:
                context['has_watermark'] = 1
            elif has_watermark == 2:
                context['has_watermark'] = 2
            else:
                return HttpResponse('Watermark problem. Wrong choice')
        except Exception as e:
            return HttpResponse('Watermark problem. err: ' + str(e))

        try:
            sign = data['sign']
            if sign == '':
                return HttpResponse('sign problem. Wrong choice')
            if sign == 1:
                context['sign'] = 1
            elif sign == 2:
                context['sign'] = 2
            elif sign == 3:
                context['sign'] = 3
            else:
                return HttpResponse('Sign problem. Wrong choice')
        except Exception as e:
            return HttpResponse('Channels problem. err: ' + str(e))

        try:
            has_image = data['img']
            if has_image == '':
                return HttpResponse('image problem. Wrong choice')
            if has_image == 0:
                context['has_image'] = 0
            elif has_image == 1:
                context['has_image'] = 1
            else:
                return HttpResponse('Snapshot problem. Wrong choice')
        except Exception as e:
            return HttpResponse('Snapshot problem. err: ' + str(e))

        SendMessageThread(context).start()
        return HttpResponse('robot been has executed')
    else:
        return HttpResponse('Not Allowed')


class SendMessageThread(threading.Thread):
    def __init__(self, context):
        threading.Thread.__init__(self)
        self.context = context

    def run(self):
        sendAlert(self.context)


class Download_Cookie(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        download_cookie()
        return print('done')

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Trading Bot!")
