from django.urls import path
from . import views

urlpatterns = [
    path('', views.discover, name='discover'),
    path('add-rate/', views.add_rate, name='add-rate'),
]
