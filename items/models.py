from django.db import models
from django.shortcuts import reverse
import random
import string

# Create your models here.

CATEGORY_CHOICES = (
    ('L', 'Ladies'),
    ('G', 'Gents'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Label(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class AccessaryLabel(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Colour(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    label = models.ManyToManyField(Label, blank=True)
    accessory_label = models.ManyToManyField(AccessaryLabel, blank=True)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    colors = models.ManyToManyField(Colour, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    image = models.ImageField()
    accessory =models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = create_ref_code()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("items:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("orders:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("orders:remove-from-cart", kwargs={
            'slug': self.slug
        })

#  class Colour(models.Model):
#         name = models.CharField(max_length=24)
#         def __str__(self):
#             return str(self.name)

#     class Size(models.Model):
#         name = models.CharField(max_length=24)
#         def __str__(self):
#             return str(self.name)

# colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
#         size = models.ForeignKey(Size, on_delete=models.CASCADE)