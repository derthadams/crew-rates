from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-rate/', views.AddRateView.as_view(), name='add-rate'),
    path('thanks/', views.thanks, name='thanks'),
]
