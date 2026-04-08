from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.officer_search, name='officer_search'),
    path('shifts/', views.shift_tracking, name='shift_tracking'),
]
