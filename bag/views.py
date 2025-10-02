from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from merch.models import Merch
from tour_dates.models import Tour_Dates


def view_bag(request):
    """A view that renders the bag contents page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_type, item_id):
    """
    Add a quantity of the specified product (merch or tour ticket) to the session bag.
    """
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', 'bag:view_bag')
    size = request.POST.get('merch_size', None)

    key = f"{item_type}_{item_id}"  # Store key in consistent format

    if item_type == "merch":
        item = Merch.objects.get(pk=item_id)
    elif item_type == "tour":
        item = Tour_Dates.objects.get(pk=item_id)
    else:
        return HttpResponse("Invalid item type", status=400)

    if size:
        if key in bag:
            if 'items_by_size' in bag[key] and size in bag[key]['items_by_size']:
                bag[key]['items_by_size'][size] += quantity
            else:
                bag[key].setdefault('items_by_size', {})[size] = quantity
        else:
            bag[key] = {'items_by_size': {size: quantity}}
    else:
        if key in bag:
            bag[key] += quantity
        else:
            bag[key] = quantity

    if item_type == "merch":
        messages.success(request, f'Added {item.name} to your bag.')
    elif item_type == "tour":
        messages.success(request, f'Added tickets for Cowboy Tanaka at {item.venue}, {item.location} to your bag.')

    request.session['bag'] = bag
    request.session.modified = True

    return redirect(redirect_url)



def adjust_bag(request, item_type, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['merch_size']
    bag = request.session.get('bag', {})
    key = f"{item_type}_{item_id}"

    if size:
        if quantity > 0:
            bag[key]['items_by_size'][size] = quantity
        else:
            del bag[key]['items_by_size'][size]
            if not bag[key]['items_by_size']:
                bag.pop(key)
    else:
        if quantity > 0:
            bag[key] = quantity
        else:
            bag.pop(key)

    request.session['bag'] = bag
    request.session.modified = True

    return redirect(reverse('bag:view_bag'))


def remove_from_bag(request, item_type, item_id):
    """ Remove an item from the shopping bag """
    try:
        bag = request.session.get('bag', {})
        key = f"{item_type}_{item_id}"
        size = request.POST.get('merch_size', None)

        if key not in bag:
            return HttpResponse("Item not found in bag", status=404)

        # Item with sizes
        if isinstance(bag[key], dict) and 'items_by_size' in bag[key]:
            if size and size in bag[key]['items_by_size']:
                del bag[key]['items_by_size'][size]
            if not bag[key]['items_by_size']:
                bag.pop(key)
        else:
            # Item without sizes
            bag.pop(key)

        request.session['bag'] = bag
        request.session.modified = True
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(f"Error removing item: {str(e)}", status=500)
