from django import forms
from .models import Tour_Dates


class TourDateForm(forms.ModelForm):

    class Meta:
        model = Tour_Dates
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        friendly_names = [(c.id, c.get_friendly_name())]

        self.fields.choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'