from django.urls import path
from . import views

urlpatterns = [
    path('features/', views.features, name='features'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
]
