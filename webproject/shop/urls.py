from django.urls import path
from shop.views.base import index_view
from shop.views.products import product_view, product_add_view


urlpatterns = [
    path('', index_view, name='index'),
    path('product/<int:pk>', product_view, name='product'),
    path('product_create/', product_add_view, name='product_add')
]