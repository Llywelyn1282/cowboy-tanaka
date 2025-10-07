from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_merch, name='merch'),
    path('<int:merch_id>/', views.merch_detail, name='merch_detail'),
    path('add/', views.add_merch, name='add_merch'),
    path('edit/<int:merch_id>', views.edit_merch, name='edit_merch'),
    path('delete/<int:merch_id>/', views.delete_merch, name='delete_merch'),
]
