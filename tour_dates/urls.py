from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tour_dates, name='tour_dates'),
    path('<int:tour_dates_id>/', views.event_detail, name='event_detail'),
    path('add/', views.add_tour_dates, name='add_tour_dates'),
]
