from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('api/type/', views.reports_by_type, name='type_stats'),
    path('api/monthly/', views.reports_by_month, name='monthly_stats'),
    path('api/status/', views.reports_by_status, name='status_stats'),
]
