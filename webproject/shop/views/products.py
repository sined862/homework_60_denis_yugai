from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product, CategoryChoices
from shop.forms import ProductForm


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    choices = CategoryChoices.choices
    return render(request, 'product.html', context={'product': product, 'choices': choices})


def product_add_view(request):
    form = ProductForm()
    if request.method == 'GET':
        context = {
            'form': form,
            'choices': CategoryChoices.choices
        }
        return render(request, 'product_create.html', context)
    form = ProductForm(request.POST)
    if not form.is_valid():
        context = {'from': form}
        return render(request, 'product_create.html', context)
    product = Product.objects.create(**form.cleaned_data)
    return redirect('product', pk=product.pk)