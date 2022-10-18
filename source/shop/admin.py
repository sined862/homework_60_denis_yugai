from django.contrib import admin
from shop.models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'balance', 'price')
    list_filter = ('id', 'title', 'description', 'category', 'balance', 'price')
    search_fields = ('title', 'description', 'category', 'balance', 'price')
    fields = ('title', 'description', 'category', 'photo', 'balance', 'price')

admin.site.register(Product, ProductAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'phone', 'address')

admin.site.register(Order, OrdersAdmin)
