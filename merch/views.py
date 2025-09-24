from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Merch


def all_merch(request):
    """ A view to show all merch, including sorting and search queries """

    merch = Merch.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('merch'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            merch = merch.filter(queries)

    category = request.GET.get('category')
    if category:
        merch = merch.filter(category__name__iexact=category)

    context = {
        'merch': merch,
        'search_term': query,
    }

    return render(request, 'merch/merch.html', context)


def merch_detail(request, merch_id):
    """ A view to show individual merch item details """

    merch = get_object_or_404(Merch, pk=merch_id)

    context = {
        'merch': merch,
    }

    return render(request, 'merch/merch_detail.html', context)