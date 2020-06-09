from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField
from django.db.models import Sum
from django.db.models.signals import post_save
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
import datetime
from django.urls import reverse_lazy
import logging
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()
# Create your models here.


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='user-images', blank=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse_lazy('user_profile', kwargs={"username": self.user.username})


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    number = PhoneNumberField(blank=True)
    city = models.CharField(max_length=100,blank=True)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
