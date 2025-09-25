from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_news, name='news'),
    path('<int:news_id>', views.post_detail, name='post_detail'),
]
