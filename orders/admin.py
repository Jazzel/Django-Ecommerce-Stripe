from django.contrib import admin

from .models import  OrderItem, Order, Refund

# Register your models here.

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


def make_being_delivered(modeladmin, request, queryset):
    queryset.update(being_delivered=True)

def make_received(modeladmin, request, queryset):
    queryset.update(received=True)


make_refund_accepted.short_description = 'Update orders to refund granted'
make_being_delivered.short_description = 'Update orders to being delivered'
make_received.short_description = 'Update orders to set received'



class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'address_shipping',
                    'address_billing',
                    ]

    def address_shipping(self,obj):
        if obj.shipping_address:
            return "Address 1: {}.\nAddress 2: {}.".format(obj.shipping_address.street_address,obj.shipping_address.apartment_address or None)

        else: 
            return "Haven't provided one yet"

    def address_billing(self,obj):
        if obj.billing_address:
            return "Address 1: {}.\nAddress 2: {}.".format(obj.billing_address.street_address,obj.billing_address.apartment_address or None)
        else: 
            return "Haven't provided one yet"


    list_display_links = [
        'user',
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted,make_being_delivered,make_received]


admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Refund)
