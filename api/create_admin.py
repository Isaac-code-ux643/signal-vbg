import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

admin_user = os.environ.get('ADMIN_USER', 'admin')
admin_pass = os.environ.get('ADMIN_PASS', 'SignalVBG2026!')
admin_email = os.environ.get('ADMIN_EMAIL', 'admin@signal-vbg.bf')

if not User.objects.filter(username=admin_user).exists():
    User.objects.create_superuser(admin_user, admin_email, admin_pass)
    print(f'Superuser "{admin_user}" cree.')
else:
    print(f'Superuser "{admin_user}" existe deja.')
