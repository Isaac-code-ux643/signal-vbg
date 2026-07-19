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
            call_command('create_admin', verbosity=0)
        except Exception:
            pass

    path = environ.get('PATH_INFO', '')

    if path == '/diag/':
        from django.conf import settings
        from django.db import connection
        tables = []
        init_status = 'not_run'
        init_error = ''
        db_cfg = settings.DATABASES['default']
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'public'"
                )
                tables = [row[0] for row in cursor.fetchall()]
            init_status = 'migrate_ok'
        except Exception as e:
            init_status = 'db_error'
            init_error = str(e)[:500]

        body = json.dumps({
            'database_url_set': bool(os.environ.get('DATABASE_URL', '')),
            'db_engine': db_cfg['ENGINE'],
            'db_host': db_cfg.get('HOST', ''),
            'db_port': db_cfg.get('PORT', ''),
            'db_user': db_cfg.get('USER', ''),
            'db_pass_len': len(db_cfg.get('PASSWORD', '')),
            'db_name': db_cfg.get('NAME', ''),
            'tables': tables,
            'init_status': init_status,
            'init_error': init_error,
        }, indent=2)
        start_response('200 OK', [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(body.encode()))),
        ])
        return [body.encode()]

    return _wsgi_app(environ, start_response)
