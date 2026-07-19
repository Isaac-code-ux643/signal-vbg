import os
import sys
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
_wsgi_app = get_wsgi_application()

_ran_init = False
_init_status = 'not_run'
_init_error = ''

def _run_init():
    global _ran_init, _init_status, _init_error
    if _ran_init:
        return
    _ran_init = True
    try:
        from django.core.management import call_command
        call_command('migrate', '--noinput', verbosity=0)
        _init_status = 'migrate_ok'
    except Exception as e:
        _init_status = 'migrate_failed'
        _init_error = traceback.format_exc()

def application(environ, start_response):
    global _init_status, _init_error

    _run_init()

    path = environ.get('PATH_INFO', '/')

    if path == '/diag/':
        import json
        from django.conf import settings
        from django.db import connection
        tables = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
                )
                tables = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            tables = ['ERROR: ' + str(e)]

        body = json.dumps({
            'database_url_set': bool(os.environ.get('DATABASE_URL', '')),
            'db_engine': settings.DATABASES['default']['ENGINE'],
            'db_host': settings.DATABASES['default'].get('HOST', ''),
            'db_port': settings.DATABASES['default'].get('PORT', ''),
            'db_user': settings.DATABASES['default'].get('USER', ''),
            'db_sslmode': settings.DATABASES['default'].get('OPTIONS', {}).get('sslmode', ''),
            'init_status': _init_status,
            'init_error': _init_error[-500:] if _init_error else '',
            'tables': tables,
        }, indent=2)
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [body.encode('utf-8')]

    return _wsgi_app(environ, start_response)
