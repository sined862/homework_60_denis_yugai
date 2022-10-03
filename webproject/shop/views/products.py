from django.shortcuts import render, get_object_or_404
from shop.models import Product, CategoryChoices


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    choices = CategoryChoices.choices
    return render(request, 'product.html', context={'product': product, 'choices': choices})