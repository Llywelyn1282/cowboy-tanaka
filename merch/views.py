from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Merch, Category
from .forms import MerchForm


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


def add_merch(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added merch!')
            return redirect(reverse('add_merch'))
        else:
            messages.error(request, 'Failed to add merch. Please ensure the form is valid.')
    else:
        form = MerchForm()
        
    template = 'merch/add_merch.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_merch(request, product_id):
    """ Edit a product in the store """
    merch = get_object_or_404(Merch, pk=product_id)
    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES, instance=merch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated merch!')
            return redirect(reverse('merch_detail', args=[merch.id]))
        else:
            messages.error(request, 'Failed to update merch. Please ensure the form is valid.')
    else:
        form = MerchForm(instance=merch)
        messages.info(request, f'You are editing {merch.name}')

    template = 'merch/edit_merch.html'
    context = {
        'form': form,
        'merch': merch,
    }

    return render(request, template, context)