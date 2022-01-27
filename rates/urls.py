from django.urls import path
from . import views

urlpatterns = [
    path('', views.discover, name='discover'),
    path(r'add-rate/', views.add_rate, name='add-rate'),
    path(r'add-rate/<path:path>', views.add_rate, name='add-rate_with_path')
]
