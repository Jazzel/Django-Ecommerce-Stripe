from django.shortcuts import render
from .models import Item
from django.views.generic import DetailView


# Create your views here.

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"