from django.urls import path
from shop.views.base import IndexView
from shop.views.products import ProductView, ProductAddView, ProductUpdateView, ProductDelView, ProductDelConfirmView
from shop.views.products import del_confirm_view, categories_view


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>', ProductView.as_view(), name='product'),
    path('product_create/', ProductAddView.as_view(), name='product_add'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('del/<int:pk>', ProductDelView.as_view(), name='product_del'),
    path('del_confirm/<int:pk>', ProductDelConfirmView.as_view(), name='product_del_confirm'),
    path('products/<str:cat>', categories_view, name='categories')
]