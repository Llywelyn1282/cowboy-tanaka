from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Tour_Dates
from .forms import TourDateForm
from django.contrib import messages


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


def add_tour_dates(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = TourDateForm(request.POST, request.FILES)
        if form.is_valid():
            tour_dates = form.save()
            messages.success(request, 'Successfully added tour date!')
            return redirect(reverse('event_detail', args=[tour_dates.id]))
        else:
            messages.error(request, 'Failed to add tour date. Please ensure the form is valid.')
    else:
        form = TourDateForm()
        
    template = 'tour_dates/add_tour_dates.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_tour_dates(request, tour_dates_id):
    """ Edit a tour_date in the store """
    tour_dates = get_object_or_404(Tour_Dates, pk=tour_dates_id)
    if request.method == 'POST':
        form = TourDateForm(request.POST, request.FILES, instance=tour_dates)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated tour date!')
            return redirect(reverse('event_detail', args=[tour_dates.id]))
        else:
            messages.error(request, 'Failed to update tour date. Please ensure the form is valid.')
    else:
        form = TourDateForm(instance=tour_dates)
        messages.info(request, f'You are editing {tour_dates.name}')

    template = 'tour_dates/edit_tour_dates.html'
    context = {
        'form': form,
        'tour_dates': tour_dates,
    }

    return render(request, template, context)


def delete_tour_dates(request, tour_dates_id):
    """ Delete a tour date item from the store """
    tour_dates = get_object_or_404(Tour_Dates, pk=tour_dates_id)
    tour_dates.delete()
    messages.success(request, 'Tour date deleted!')
    return redirect(reverse('tour_dates'))