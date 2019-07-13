from django.db import models


# Create your models here.
class SMS(models.Model):
    url_campaign = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='')
    visit_count = models.IntegerField(default=0)
