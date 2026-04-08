from django.urls import path
from . import views

urlpatterns = [
    path('', views.criminal_list, name='criminal_list'),
    path('<int:criminal_id>/', views.criminal_profile, name='criminal_profile'),
    path('repeat-offenders/', views.repeat_offenders, name='repeat_offenders'),
]
