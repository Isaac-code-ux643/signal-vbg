import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
_wsgi_app = get_wsgi_application()

_ran_init = False
_init_status = None
_init_error = None

def application(environ, start_response):
    global _ran_init, _init_status, _init_error

    path = environ.get('PATH_INFO', '/')

    if path == '/diag/':
        import json
        from django.conf import settings
        db_engine = settings.DATABASES['default']['ENGINE']
        db_name = settings.DATABASES['default'].get('NAME', '')
        has_url = bool(os.environ.get('DATABASE_URL', ''))
        body = json.dumps({
            'database_url_set': has_url,
            'db_engine': db_engine,
            'db_name': db_name,
            'init_status': _init_status,
            'init_error': _init_error,
        }, indent=2)
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [body.encode('utf-8')]

    if not _ran_init:
        _ran_init = True
        try:
            from django.core.management import call_command
            try:
                call_command('migrate', '--noinput', verbosity=2)
                _init_status = 'migrate_ok'
            except Exception as e:
                _init_status = 'migrate_failed'
                _init_error = str(e)
            if _init_status == 'migrate_ok':
                try:
                    call_command('seed_centers', verbosity=0)
                    call_command('create_admin', verbosity=0)
                except Exception:
                    pass
        except Exception as e:
            _init_status = 'setup_failed'
            _init_error = str(e)

    return _wsgi_app(environ, start_response)
