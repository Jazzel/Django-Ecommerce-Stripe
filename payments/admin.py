from django.contrib import admin
from payments.models import Payment, Coupon
from django.utils.html import format_html
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'option','order_link','items', 'amount',
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

admin.site.register(Payment,PaymentAdmin)   