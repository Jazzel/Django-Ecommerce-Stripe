from django.contrib import admin
from .models import  Address
# Register your models here.

admin.site.site_header = "All Classic Footwear"


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'number',
        'city',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'city']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Address, AddressAdmin)
