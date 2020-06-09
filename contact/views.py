from django.shortcuts import render
from django.views.generic import CreateView
from .forms import ContactForm
from .models import Contact
from items.models import Label,AccessaryLabel   
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.


class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Message delivered to admins. Someone will contact you soon !!")
        return HttpResponseRedirect('/contact/')

    def get_context_data(self, **kwargs):
        context = super(ContactCreateView, self).get_context_data(**kwargs)
        context['head'] = 'Contact'
        context['slider_head'] = 'Contact Us'
        context['slider_sub_head'] = ''
        context['slider_image'] = '/static/static/img/contact.jpg'
        context['men_links'] = Label.objects.filter(categories__name='Men')
        context['women_links'] = Label.objects.filter(categories__name='Women')
        context['kids_links'] = Label.objects.filter(categories__name='Kids')
        context['acc_labels']= AccessaryLabel.objects.all()
        return context

