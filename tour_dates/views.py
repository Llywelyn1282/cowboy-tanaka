from django.shortcuts import render, get_object_or_404
from .models import Tour_Dates


def all_tour_dates(request):
    """ A view to show all tour dates, including sorting and search queries """

    tour_dates = Tour_Dates.objects.all()

    context = {
        'tour_dates': tour_dates,
    }

    return render(request, 'tour_dates/tour_dates.html', context)


def event_detail(request, tour_dates_id):
    """ A view to show individual event details """

    tour_dates = get_object_or_404(Tour_Dates, pk=tour_dates_id)

    context = {
        'tour_dates': tour_dates,
    }

    return render(request, 'tour_dates/event_detail.html', context)