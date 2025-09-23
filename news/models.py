from django.db import models

class News(models.Model):
    class Meta:
        verbose_name_plural = 'News'

    title = models.CharField(max_length=254)
    subtitle = models.TextField()
    excerpt = models.TextField()
    post = models.TextField()
    author = models.CharField(max_length=254)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title