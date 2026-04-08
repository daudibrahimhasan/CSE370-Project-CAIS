from django.urls import path
from . import views

urlpatterns = [
    path('', views.crime_list, name='crime_list'),
    path('pattern-finder/', views.pattern_finder, name='pattern_finder'),
    path('<int:crime_id>/', views.crime_detail, name='crime_detail'),
]
