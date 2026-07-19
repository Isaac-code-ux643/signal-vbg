import os
import sys
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

try:
    import django
    django.setup()

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

except Exception:
    traceback.print_exc()

    def application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [b'<h1>Server Error</h1><p>Application failed to start. Check Vercel logs.</p>']
