from django.shortcuts import render, redirect


def view_bag(request):
    """A view that renders the bag contents page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_type, item_id):
    """
    Add a quantity of the specified product (merch or tour  ticket) to the session bag.

    Parameters:
    - item_type: 'merch' or 'tour'
    - item_id: primary key of the item
    """
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', 'bag:view_bag')
    size = request.POST.get('product_size', None)

    bag = request.session.get('bag', {})

    key = f"{item_type}_{item_id}"  # Store key in consistent format

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

    request.session['bag'] = bag
    request.session.modified = True

    return redirect(redirect_url)
