from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create Staff User"

    def handle(self, *args, **kwargs):
        user = User.objects.create(username="xpay", is_staff="True")
        user.set_password("xpay")
        user.save()
        self.stdout.write("create staff user with username xpay and password xpay")