from math import prod
from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product, CategoryChoices
from shop.forms import ProductForm, SearchForm


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    choices = CategoryChoices.choices
    return render(request, 'product.html', context={'product': product, 'choices': choices})


def product_add_view(request):
    choices = CategoryChoices.choices
    form = ProductForm()
    if request.method == 'GET':
        context = {
            'form': form,
            'choices': choices
        }
        return render(request, 'product_create.html', context)
    form = ProductForm(request.POST)
    if not form.is_valid():
        context = {'form': form, 'choices': choices}
        return render(request, 'product_create.html', context)
    product = Product.objects.create(**form.cleaned_data)
    return redirect('product', pk=product.pk)


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    choices = CategoryChoices.choices
    if request.method == 'GET':
        form = ProductForm(initial={
            'title': product.title,
            'description': product.description,
            'category': product.category,
            'photo': product.photo,
            'balance': product.balance,
            'price': product.price
        })
        return render(request, 'product_update.html', context={'form': form, 'product': product, 'choices': choices})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.title = form.cleaned_data['title']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.photo = form.cleaned_data['photo']
            product.balance = form.cleaned_data['balance']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('product', pk=product.pk)
        else:
            return render(request, 'product_update.html', context={'form': form, 'product': product, 'choices': choices})


def del_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'confirm_delete.html', context)


def del_confirm_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('index')


def categories_view(request, cat):
    form = SearchForm()
    choices = CategoryChoices.choices
    if request.method == 'GET':
        if not request.GET.get('title'):
            products = Product.objects.filter(category=cat, balance__gte = 1)
            context = {
                'products': products,
                'choices': choices,
                'form': form,
                'cat': cat
            }
            return render(request, 'categories.html', context)
        products = Product.objects.filter(category=cat, balance__gte = 1, title=request.GET.get('title'))
        error = 'Ни одной записи не найдено'
        context = {
            'products': products,
            'form': form,
            'error': error,
            'choices': choices,
            'cat': cat
        }
        return render(request, 'categories.html', context)

            