from django.shortcuts import render, get_object_or_404
from .models import News


def all_news(request):
    """ A view to show all news, including sorting and search queries """

    news = News.objects.all()

    context = {
        'news': news,
    }

    return render(request, 'news/news.html', context)



def post_detail(request, news_id):
    """ A view to show individual news post details """

    news = get_object_or_404(News, pk=news_id)

    context = {
        'news': news,
    }

    return render(request, 'news/post_detail.html', context)