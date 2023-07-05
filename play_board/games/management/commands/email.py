from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'update email'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not user.email:
                user.email = None
                user.save()
