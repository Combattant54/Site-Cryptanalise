from django.db import models
from django.urls import reverse

# Create your models here.
class MiniURL(models.Model):
    long_url = models.URLField(unique=True, verbose_name="L'URL vers laquelle pointe le raccourci")
    url_code = models.CharField(unique=True, max_length=20, verbose_name="Le code du raccourci")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    creator = models.CharField(max_length=50, verbose_name="Le pseudo du créateur du raccourci", blank=True, default="")
    access_amount = models.IntegerField(verbose_name="Le nombre d'accès au raccourci", default=0)
    
    def get_absolute_url(self):
        url = reverse('mini_url.redirect', kwargs={'url_code': self.url_code})
        print(url)
        return url
