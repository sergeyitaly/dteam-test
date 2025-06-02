from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'main'

router = DefaultRouter()
router.register(r'cvs', views.CVViewSet, basename='cv')

urlpatterns = [
    path('', views.cv_list, name='cv_list'),
    path('<int:pk>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:pk>/pdf/', views.cv_pdf, name='cv_pdf'),
    path('api/', include(router.urls)), 
    path('settings/', views.SettingsView.as_view(), name='settings-view'),

]
