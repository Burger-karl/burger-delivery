from django.db import models
from users.models import User

# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    recipient_address = models.CharField(max_length=255)
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rider', null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    has_rider = models.BooleanField(default=False)
