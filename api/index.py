import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
_wsgi_app = get_wsgi_application()

_ran_init = False

def application(environ, start_response):
    global _ran_init
    if not _ran_init:
        _ran_init = True
        try:
            from django.core.management import call_command
            call_command('migrate', '--noinput', verbosity=0)
            call_command('seed_centers', verbosity=0)
            call_command('seed_resources', verbosity=0)
            call_command('create_admin', verbosity=0)
        except Exception:
            pass
    return _wsgi_app(environ, start_response)
