from django.http import HttpResponse
from merch.models import Merch
from tour_dates.models import Tour_Dates
from checkout.models import Order, OrderLineItem
import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.country,
                    postcode__iexact=shipping_details.postal_code,
                    town_or_city__iexact=shipping_details.city,
                    street_address1__iexact=shipping_details.line1,
                    street_address2__iexact=shipping_details.line2,
                    county__iexact=shipping_details.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
            if order_exists:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                    status=200)
            else:
                order=None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=shipping_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.country,
                        postcode=shipping_details.postal_code,
                        town_or_city=shipping_details.city,
                        street_address1=shipping_details.line1,
                        street_address2=shipping_details.line2,
                        county=shipping_details.state,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    for item_id, item_data in json.bag_data.items():
                        try:
                            # Determine item type based on prefix (merch_# or tour_#)
                            if isinstance(item_id, str) and item_id.startswith('tour_'):
                                numeric_id = int(item_id.split('_')[1])
                                product = Tour_Dates.objects.get(id=numeric_id)
                                item_type = 'tour'
                            else:
                                numeric_id = int(item_id.split('_')[1])
                                product = Merch.objects.get(id=numeric_id)
                                item_type = 'merch'

                            # Handle simple quantity
                            if isinstance(item_data, int):
                                OrderLineItem.objects.create(
                                    order=order,
                                    merch=product if item_type == 'merch' else None,
                                    tour_dates=product if item_type == 'tour' else None,
                                    quantity=item_data,
                                )

                            # Handle items with sizes (for merch)
                            elif isinstance(item_data, dict) and 'items_by_size' in item_data:
                                for size, quantity in item_data['items_by_size'].items():
                                    OrderLineItem.objects.create(
                                        order=order,
                                        merch=product if item_type == 'merch' else None,
                                        tour_dates=product if item_type == 'tour' else None,
                                        product_size=size,
                                        quantity=quantity,
                                    )

                        except (Merch.DoesNotExist, Tour_Dates.DoesNotExist):
                            if order:
                                order.delete()
                            return HttpResponse(
                                content=f'Webhook received: {event["type"]} | ERROR: Item not found',
                                status=500
                            )

                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500
                    )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Payment failed',
            status=200
        )
