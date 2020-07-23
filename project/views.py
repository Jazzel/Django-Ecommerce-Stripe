from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView
from items.models import Colour, Item, Size, Label,AccessaryLabel
import random
import string
from orders.models import OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def get_or_none(classModel, **kwargs):
    try:
        return classModel.objects.get(**kwargs)
    except classModel.DoesNotExist:
        return None

class HomeView(ListView):
    model = Item
    # paginate_by = 10
    template_name = "home.html"

    def get_queryset(self):
        queryset = Item.objects.all()[:4]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeView,
                        self).get_context_data(**kwargs)
        context['men_links'] = Label.objects.filter(categories__name='Men')
        context['women_links'] = Label.objects.filter(categories__name='Women')
        context['kids_links'] = Label.objects.filter(categories__name='Kids')
        hot_sales = OrderItem.objects.values_list('item_id', flat=True).distinct()[:4]
        item_objects=[]
        for item_id in hot_sales:
            item = Item.objects.get(id=item_id)
            item_object = {
                "title":item.title,
                "price":item.price,
                "discount_price":item.discount_price,
                "image":item.image.url,
                "get_absolute_url":item.get_absolute_url,
                
            }
            item_objects.append(item_object)
        context['sales'] = item_objects

        context['acc_labels']= AccessaryLabel.objects.all()
        context['sizes'] = Size.objects.all()


        return context

class CutSize(ListView):
    model = Item
    # paginate_by = 10

    def get(self, *arg, **kwargs):
        label = ''
        queryset = ''
        try:
            if kwargs['size']:
                label = kwargs['size']
                queryset = Item.objects.filter(sizes__name=label)
        
        except:
            queryset = None

        hot_sales = OrderItem.objects.values_list('item_id', flat=True).distinct()[:4]
        item_objects=[]
        for item_id in hot_sales:
            item = Item.objects.get(id=item_id)
            item_object = {
                "title":item.title,
                "price":item.price,
                "discount_price":item.discount_price,
                "image":item.image.url,
                "get_absolute_url":item.get_absolute_url,
            }
            item_objects.append(item_object)

        context = {
            # 'category':category,
            'colors' : Colour.objects.all(),
            'sizes' : Size.objects.all(),
            'acc_labels': AccessaryLabel.objects.all(),
            'men_links' : Label.objects.filter(categories__name='Men'),
            'women_links' : Label.objects.filter(categories__name='Women'),
            'kids_links' : Label.objects.filter(categories__name='Kids'),
            'sales': item_objects,
            'object_list':queryset,
            # 'size':get_or_none(Size ,name=size),
            # 'color': get_or_none(Colour ,name=color),
            'label': label,
        }

        return render(self.request, "cutsize.html", context)




class ItemsCategoryView(ListView):
    model = Item
    template_name = "categories.html"

    def get(self, *arg, **kwargs):
        size = self.request.GET.get('size')
        color = self.request.GET.get('color')
        category = kwargs['category']
        label = ''
        try:
            if kwargs['label']:
                label = kwargs['label']
                if size:
                    queryset = Item.objects.filter(label__name=label, categories__name=category,sizes__name=size,accessory=False)
                elif color:
                    queryset = Item.objects.filter(label__name=label, categories__name=category,colors__name=color,accessory=False)
                else:
                    queryset = Item.objects.filter(label__name=label, categories__name=category,accessory=False)
        
        except:
            if size:
                queryset = Item.objects.filter(categories__name=category,sizes__name=size,accessory=False)
            elif color:
                queryset = Item.objects.filter(categories__name=category,colors__name=color,accessory=False)
            else:
                    queryset = Item.objects.filter(categories__name=category,accessory=False)

        hot_sales = OrderItem.objects.values_list('item_id', flat=True).distinct()[:4]
        item_objects=[]
        for item_id in hot_sales:
            item = Item.objects.get(id=item_id)
            item_object = {
                "title":item.title,
                "price":item.price,
                "discount_price":item.discount_price,
                "image":item.image.url,
                "get_absolute_url":item.get_absolute_url,
            }
            item_objects.append(item_object)

        context = {
            'category':category,
            'colors' : Colour.objects.all(),
            'sizes' : Size.objects.all(),
            'acc_labels': AccessaryLabel.objects.all(),
            'men_links' : Label.objects.filter(categories__name='Men'),
            'women_links' : Label.objects.filter(categories__name='Women'),
            'kids_links' : Label.objects.filter(categories__name='Kids'),
            'sales': item_objects,
            'object_list':queryset,
            'size':get_or_none(Size ,name=size),
            'color': get_or_none(Colour ,name=color),
            'label': label,
        }

        return render(self.request, "categories.html", context)



class AccCategoryView(ListView):
    model = Item

    def get(self, *arg, **kwargs):
        label = ''
        try:
            if kwargs['label']:
                label = kwargs['label']
                queryset = Item.objects.filter(acc_label__name=label,accessory=True)
        
        except:
            queryset = Item.objects.filter(accessory=True)

        hot_sales = OrderItem.objects.values_list('item_id', flat=True).distinct()[:4]
        item_objects=[]
        for item_id in hot_sales:
            item = Item.objects.get(id=item_id)
            item_object = {
                "title":item.title,
                "price":item.price,
                "discount_price":item.discount_price,
                "image":item.image.url,
                "get_absolute_url":item.get_absolute_url,
            }
            item_objects.append(item_object)
        context = {
            'colors' : Colour.objects.all(),
            'sizes' : Size.objects.all(),
            'acc_labels': AccessaryLabel.objects.all(),
            'men_links' : Label.objects.filter(categories__name='Men'),
            'women_links' : Label.objects.filter(categories__name='Women'),
            'kids_links' : Label.objects.filter(categories__name='Kids'),
            'sales' : item_objects,
            'object_list':queryset,
            'label':label
        }

        return render(self.request, "a_categories.html", context)

class ContactView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context["sizes"] = Size.objects.all()
        return context
    
    
    
class OrdersView(ListView,LoginRequiredMixin):
    model=Order
    template_name = "my-orders.html"

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by("-start_date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        context['men_links'] = Label.objects.filter(categories__name='Men')
        context['women_links'] = Label.objects.filter(categories__name='Women')
        context['kids_links'] = Label.objects.filter(categories__name='Kids')
        context['acc_labels']= AccessaryLabel.objects.all()
        context["sizes"] =  Size.objects.all()

        return context
    