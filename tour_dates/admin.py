from django.contrib import admin
from .models import Tour_Dates


class Tour_Dates_Admin(admin.ModelAdmin):
    list_display = (
        'date',
        'venue',
        'location',
        'support_act',
        'image',
    )

    ordering = ('date',)


admin.site.register(Tour_Dates, Tour_Dates_Admin)
