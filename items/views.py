from django.shortcuts import render
from .models import Item
from django.views.generic import DetailView

from items.models import Label,AccessaryLabel   

# Create your views here.

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['men_links'] = Label.objects.filter(categories__name='Men')
        context['women_links'] = Label.objects.filter(categories__name='Women')
        context['kids_links'] = Label.objects.filter(categories__name='Kids')
        context['acc_labels']= AccessaryLabel.objects.all()
        return context