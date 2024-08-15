from django.urls import path

from tradingview.views import webhook_view, cookie_reset_view
from django.views.decorators.csrf import csrf_exempt

app_name = 'tradingview'

urlpatterns = [
    path('post/key=<str:key>/', csrf_exempt(webhook_view), name='webhook'),
    path('reset/key=<str:key>/', csrf_exempt(cookie_reset_view), name='cookie'),
]
