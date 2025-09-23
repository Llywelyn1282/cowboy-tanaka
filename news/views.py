from django.shortcuts import render
from .models import News


def all_news(request):
    """ A view to show all news, including sorting and search queries """

    news = News.objects.all()

    context = {
        'news': news,
    }

    return render(request, 'news/news.html', context)
