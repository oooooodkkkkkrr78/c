from django.db import models


class LoggerDebug(models.Model):
    log = models.CharField(max_length=2000, verbose_name="log")

    def __str__(self):
        return self.log

    class Meta:
        verbose_name = "log - debug"
        verbose_name_plural = "logs - debug"


class LoggerProduction(models.Model):
    log = models.CharField(max_length=2000, verbose_name="log")

    def __str__(self):
        return self.log

    class Meta:
        verbose_name = "log - production"
        verbose_name_plural = "logs - production"
