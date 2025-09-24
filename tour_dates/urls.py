from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tour_dates, name='tour_dates'),
]
