from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from merch.models import Merch
from tour_dates.models import Tour_Dates
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()

            # --- Safe bag handling ---
            for item_id, item_data in bag.items():
                try:
                    # Determine item_type safely
                    if isinstance(item_data, dict) and 'item_type' in item_data:
                        item_type = item_data['item_type']
                    elif isinstance(item_id, str):
                        if item_id.startswith('tour_'):
                            item_type = 'tour'
                        else:
                            item_type = 'merch'
                    else:
                        item_type = 'merch'

                    # Extract numeric ID
                    numeric_id = int(item_id.split('_')[-1]) if isinstance(item_id, str) else item_id

                    # Fetch product
                    if item_type == 'merch':
                        product = Merch.objects.get(pk=numeric_id)
                    else:  # tour
                        product = Tour_Dates.objects.get(pk=numeric_id)

                    # Handle quantities and sizes
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            merch=product if item_type == 'merch' else None,
                            tour_dates=product if item_type == 'tour' else None,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    elif isinstance(item_data, dict) and 'items_by_size' in item_data:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                merch=product if item_type == 'merch' else None,
                                tour_dates=product if item_type == 'tour' else None,
                                product_size=size,
                                quantity=quantity,
                            )
                            order_line_item.save()
                    else:
                        continue

                except (Merch.DoesNotExist, Tour_Dates.DoesNotExist):
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save info checkbox
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle successful checkouts """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! '
        f'Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
