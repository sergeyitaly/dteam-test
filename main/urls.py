from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.cv_list, name='cv_list'),       
    path('<int:pk>/', views.cv_detail, name='cv_detail'), 
]
