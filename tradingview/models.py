from django.db import models


class Watermark(models.Model):
    watermark = models.ImageField(upload_to='watermark', null=False, blank=False, verbose_name='watermark')

    def __str__(self):
        return self.watermark.path

    class Meta:
        verbose_name = 'watermark'
        verbose_name_plural = 'watermarks'


# class Snapshot(models.Model):
#     pure_image = models.ImageField(upload_to='snapshot', null=False, blank=False, verbose_name='image')
#     watermarked_image = models.ImageField(upload_to='snapshot_watermarked', null=True, blank=True,
#                                           verbose_name='watermarked image')
#
#     def __str__(self):
#         return self.pure_image.path
#
#     class Meta:
#         verbose_name = 'image gallery'
#         verbose_name_plural = 'image gallery'


class Setting(models.Model):
    watermark = models.ForeignKey(Watermark, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='watermark')

    def __str__(self):
        return self.watermark

    class Meta:
        verbose_name = 'setting'
        verbose_name_plural = 'settings'


class TelegramSetting(models.Model):
    bot_token = models.CharField(max_length=255, null=False, blank=False, verbose_name='bot token')
    channel_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='channel name')

    def __str__(self):
        return self.bot_token

    class Meta:
        verbose_name = 'channel and robot'
        verbose_name_plural = 'channels and robots'


class Key(models.Model):
    secure_key = models.CharField(max_length=255, null=False, blank=False, verbose_name='secure key')

    def __str__(self):
        return self.secure_key

    class Meta:
        verbose_name = 'Webhook secure key'
        verbose_name_plural = 'Webhook secure keys'


class LoginCookie(models.Model):
    user_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='user name')
    password = models.CharField(max_length=255, null=False, blank=False, verbose_name='password')
    cookies = models.TextField(null=True, blank=True, editable=False, verbose_name='اطلاعات کوکی')
    date_time = models.DateTimeField(auto_now=True, verbose_name="cookie's saving time")

    def __str__(self):
        return "Tradingview login detail is " + self.user_name + " : " + self.password

    class Meta:
        verbose_name = "login's cookie"
        verbose_name_plural = "login's cookies"
