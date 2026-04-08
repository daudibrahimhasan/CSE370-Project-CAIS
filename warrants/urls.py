from django.urls import path
from . import views

urlpatterns = [
    path('', views.warrant_tracking, name='warrant_tracking'),
    path('bolo/', views.bolo_list, name='bolo_list'),
]
