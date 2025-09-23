from django.shortcuts import render
from .models import Merch


def all_merch(request):
    """ A view to show all merch, including sorting and search queries """

    merch = Merch.objects.all()

    context = {
        'merch': merch,
    }

    return render(request, 'merch/merch.html', context)
