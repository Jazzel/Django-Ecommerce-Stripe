from django.db import models
from django.urls import reverse
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=100, blank=False)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('home')
