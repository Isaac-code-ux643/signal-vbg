from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create admin superuser if not exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@signal-vbg.bf'
        password = 'SignalVBG2026!'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'"{username}" existe deja.'))
        else:
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" cree.'))
