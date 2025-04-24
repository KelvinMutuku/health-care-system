from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('client/<int:client_id>/', views.client_profile, name='client_profile'),
    path('add-client/', views.add_client, name='add_client'),
    path('enroll-client/', views.enroll_client, name='enroll_client'),
]
