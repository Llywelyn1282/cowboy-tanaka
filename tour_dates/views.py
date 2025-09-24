from django.shortcuts import render
from .models import Tour_Dates


def all_tour_dates(request):
    """ A view to show all tour dates, including sorting and search queries """

    tour_dates = Tour_Dates.objects.all()

    context = {
        'tour_dates': tour_dates,
    }

    return render(request, 'tour_dates/tour_dates.html', context)
