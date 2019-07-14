from django.db import models


# Create your models here.
class SMS(models.Model):
    campaign = models.CharField(max_length=100, default='')
    campaign_code = models.CharField(max_length=50, default='')
    link_campaign = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    phone = models.CharField(max_length=20, default='')
    sms_status = models.CharField(max_length=50, default='')
    tracking_report = models.CharField(max_length=50, default='')
    pic = models.CharField(max_length=100, default='')
    sale_status = models.CharField(max_length=100, default='')
    visit_count = models.IntegerField(default=0)
