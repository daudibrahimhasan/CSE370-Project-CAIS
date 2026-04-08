from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_status_list, name='case_status_list'),
    path('<int:case_id>/', views.case_detail, name='case_detail'),
]
