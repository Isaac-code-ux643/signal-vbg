from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('connexion/', views.login_view, name='login'),
    path('inscription/', views.register_view, name='register'),
    path('deconnexion/', LogoutView.as_view(), name='logout'),
]
