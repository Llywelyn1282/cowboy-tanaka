from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )
        widgets = {
            'country': CountrySelectWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_config = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
            'country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for name, field in self.fields.items():
            label = field_config.get(name, name.replace('_', ' ').title())

            # Add accessible name (required since labels are hidden)
            field.widget.attrs['aria-label'] = label

            # Add placeholder only to text inputs
            if name != 'country':
                if field.required:
                    label = f'{label} *'
                field.widget.attrs['placeholder'] = label

            field.widget.attrs['class'] = 'stripe-style-input'
            field.label = False
