from django.shortcuts import render, redirect


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_type, item_id):
    """
    Add a quantity of a merch or tour ticket to the session bag.
    item_type: 'merch' or 'tour'
    item_id: primary key of the item
    """
    bag = request.session.get('bag', {})

    key = f"{item_type}_{item_id}"  # always store in new format
    quantity = int(request.POST.get('quantity', 1))

    if key in bag:
        bag[key] += quantity
    else:
        bag[key] = quantity

    request.session['bag'] = bag
    request.session.modified = True

    return redirect('bag:view_bag')
