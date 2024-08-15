from django.contrib import admin

from tradingview.models import Watermark, TelegramSetting, Key, LoginCookie


@admin.register(Watermark)
class WatermarkAdmin(admin.ModelAdmin):
    list_display = (
        'watermark',
    )

    fields = (
        'watermark',
    )


@admin.register(TelegramSetting)
class TelegramSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bot_token',
        'channel_name'
    )

    fields = (
        'bot_token',
        'channel_name'
    )


# @admin.register(Snapshot)
# class SnapshotAdmin(admin.ModelAdmin):
#     list_display = (
#         'pure_image',
#         'watermarked_image',
#     )
#
#     fields = (
#         'pure_image',
#         'watermarked_image',
#     )


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = (
        'secure_key',
    )

    fields = (
        'secure_key',
    )


@admin.register(LoginCookie)
class LoginCookieAdmin(admin.ModelAdmin):
    list_display = (
        'user_name',
        'password',
        'date_time',
    )
    readonly_fields = (
        'date_time',
        'cookies',
    )

    fields = (
        'user_name',
        'password',
        'cookies',
        'date_time',
    )