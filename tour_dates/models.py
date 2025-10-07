from django.db import models


class Tour_Dates(models.Model):
    class Meta:
        verbose_name_plural = 'Tour Dates'
        ordering = ['date']

    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    venue = models.CharField(max_length=254)
    location = models.CharField(max_length=254)
    support_act = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.venue
