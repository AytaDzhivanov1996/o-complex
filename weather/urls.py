from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history_city_count/', views.history_city_count, name='history_city_count'),
    path('history/', views.history, name='history'),
    path('autocomplete/', views.autocomplete, name='autocomplete')
]