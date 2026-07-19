from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('faq/', views.faq_list, name='faq'),
    path('api/chatbot/', views.chatbot_api, name='chatbot'),
    path('', views.resource_list, name='list'),
]
