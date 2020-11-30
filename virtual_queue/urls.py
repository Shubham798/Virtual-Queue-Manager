from django.urls import path
from . import views

urlpatterns = [
    path('host/', views.host_home),
    path('host/register', views.host_register),
    path('host/login', views.host_login),

    path('join/', views.join_home),
    path('join/register', views.join_register),
    path('join/login', views.join_login),

    path('join/join-request', views.join_request),
    path('host/delete-request', views.delete_request),

    path('logout/', views.logout_request),
]
