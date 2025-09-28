from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from merch.models import Merch
from tour_dates.models import Tour_Dates

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})


    # Delivery charge
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
