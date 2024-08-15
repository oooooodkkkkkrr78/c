from django.core.management import BaseCommand
from logger.views import LoggerDebug


class Command(BaseCommand):
    def handle(self, *args, **options):
        LoggerDebug.objects.all().delete()
