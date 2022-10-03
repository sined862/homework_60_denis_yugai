from django.urls import path
from shop.views.base import index_view
from shop.views.products import product_view


urlpatterns = [
    path('', index_view, name='index'),
    path('product/<int:pk>', product_view, name='product')
]