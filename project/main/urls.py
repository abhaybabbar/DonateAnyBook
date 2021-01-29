from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main_home'),
    path('donate', views.donate, name='main_donate'),
    path('result/', views.result, name='result'),
]