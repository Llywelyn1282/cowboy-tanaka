from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from merch.models import Merch
from tour_dates.models import Tour_Dates

def bag_contents(request):
    """
    Context processor that returns the shopping bag contents.
    Supports both Merch and Tour_Dates items.
    Skips any invalid/missing objects.
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for key, quantity in bag.items():
        # new format e.g. "merch_1" or "tour_5"
        if '_' in key:
            item_type, item_id = key.split('_')
            try:
                item_id = int(item_id)
            except ValueError:
                continue  # skip invalid key

            if item_type == 'merch':
                try:
                    merch = get_object_or_404(Merch, pk=item_id)
                except:
                    continue  # skip missing item
                total += quantity * merch.price
                product_count += quantity
                bag_items.append({
                    'item_id': key,
                    'quantity': quantity,
                    'merch': merch,
                    'tour_dates': None,
                })

            elif item_type == 'tour':
                try:
                    tour_date = get_object_or_404(Tour_Dates, pk=item_id)
                except:
                    continue  # skip missing item
                total += quantity * tour_date.price
                product_count += quantity
                bag_items.append({
                    'item_id': key,
                    'quantity': quantity,
                    'merch': None,
                    'tour_dates': tour_date,
                })


    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
