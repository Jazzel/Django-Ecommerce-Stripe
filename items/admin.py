from django.contrib import admin

# Register your models here.

from .models import Item, Category, Colour, Size, Label,AccessaryLabel

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("slug", )
        form = super(ItemAdmin, self).get_form(request, obj, **kwargs)
        return form




admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Colour)
admin.site.register(Label)
admin.site.register(Size)
admin.site.register(AccessaryLabel)