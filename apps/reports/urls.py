from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.home, name='home'),
    path('signaler/', views.submit_report, name='submit'),
    path('rechercher/', views.search_report, name='search'),
]
