import os
import sys
import threading

_migrated = False
_lock = threading.Lock()


def auto_migrate(get_response):
    global _migrated

    def middleware(request):
        global _migrated
        if not _migrated:
            with _lock:
                if not _migrated:
                    try:
                        from django.core.management import call_command
                        call_command('migrate', '--run-syncdb', verbosity=0)
                        _migrated = True
                    except Exception:
                        pass
        return get_response(request)

    return middleware
