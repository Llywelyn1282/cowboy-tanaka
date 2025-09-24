from django.shortcuts import render, get_object_or_404
from .models import Merch


def all_merch(request):
    """ A view to show all merch, including sorting and search queries """

    merch = Merch.objects.all()

    context = {
        'merch': merch,
    }

    return render(request, 'merch/merch.html', context)


def merch_detail(request, merch_id):
    """ A view to show individual merch detail """

    merch = get_object_or_404(Merch, pk=merch_id)

    context = {
        'merch': merch,
    }

    return render(request, 'merch/merch_detail.html', context)
