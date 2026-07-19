from django.urls import path
from . import views

app_name = 'centers'

urlpatterns = [
    path('carte/', views.centers_map, name='map'),
    path('api/json/', views.centers_json, name='json'),
    path('<int:pk>/', views.center_detail, name='detail'),
]
