from django.contrib import admin
from payments.models import Payment, Coupon
from django.utils.html import format_html
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'option','order_link','items', 'amount','contact_number', 'city'
    )
    list_filter = ['option']
    search_fields = ['user']

    def order_link(self, obj):
        return format_html('<a href="/admin/orders/order/{url}">{url}</a>', url=obj.order.id)
    order_link.allow_tags = True

    def items(self,obj):
        data = ""
        for item in obj.order.items.all():
            data += "<a href='/admin/orders/orderitem/{}'>Item: {}, Color:{}<a> \n".format(item.id,item,item.color)
        return format_html(data)
    
    def contact_number(self,obj):
        return obj.order.shipping_address.number

    def city(self,obj):
        return obj.order.shipping_address.city

admin.site.register(Payment,PaymentAdmin)   