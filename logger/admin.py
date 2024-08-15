from django.contrib import admin
from logger.models import LoggerProduction, LoggerDebug


@admin.register(LoggerProduction)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("log",)
    ordering = ("-id",)
    search_fields = ["log", ]

    fields = (
        'log',
    )


@admin.register(LoggerDebug)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("log",)
    ordering = ("-id",)
    search_fields = ["log", ]

    fields = (
        'log',
    )
