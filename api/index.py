import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

try:
    from django.core.management import call_command
    call_command('migrate', verbosity=0)
except Exception:
    pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
