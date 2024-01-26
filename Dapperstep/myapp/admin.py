from django.contrib import admin
from . models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'img']
    list_editable = ['price', 'stock', 'img']
    list_filter = ['price']
    search_fields = ['name', 'price']



admin.site.register(UserProfile)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)


