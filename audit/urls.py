from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('logs/', views.recent_requests, name='recent_requests'),
]
