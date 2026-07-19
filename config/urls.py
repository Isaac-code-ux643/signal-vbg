from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.reports.urls', namespace='reports')),
    path('suivi/', include('apps.tracking.urls', namespace='tracking')),
    path('centres/', include('apps.centers.urls', namespace='centers')),
    path('ressources/', include('apps.resources.urls', namespace='resources')),
    path('tableau-de-bord/', include('apps.dashboard.urls', namespace='dashboard')),
    path('compte/', include('apps.accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
