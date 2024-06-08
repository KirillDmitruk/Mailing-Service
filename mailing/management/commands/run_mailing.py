from django.core.management import BaseCommand
from mailing.services import send_mails


class Command(BaseCommand):
    """Команда запуска рассылки из консоли"""
    def handle(self, *args, **options):
        send_mails()
        