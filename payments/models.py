from django.db import models
from orders.models import Order
from django.conf import settings

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField()
    option= models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    
    


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

