from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('cas/', views.cases_list, name='cases'),
    path('cas/<int:report_id>/', views.case_detail, name='case_detail'),
    path('cas/<int:report_id>/statut/', views.case_update_status, name='case_update_status'),
    path('api/type/', views.reports_by_type, name='type_stats'),
    path('api/monthly/', views.reports_by_month, name='monthly_stats'),
    path('api/status/', views.reports_by_status, name='status_stats'),
]
