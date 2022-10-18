﻿from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product, CategoryChoices, ProductInCart
from shop.forms import ProductForm, SearchForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy



class ProductView(DetailView):
    template_name = 'product.html'
    model = Product
    extra_context = {'choices': CategoryChoices.choices}


class ProductAddView(CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm
    extra_context = {'choices': CategoryChoices.choices}

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm
    extra_context = {'choices': CategoryChoices.choices}

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.pk})


class ProductDelView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Product

    def get_success_url(self):
        return reverse('product_del', kwargs={'pk': self.object.pk})

def to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    balance = product.balance
    if balance > 0:
        if ProductInCart.objects.filter(product_id=pk).exists():
            product_in = ProductInCart.objects.get(product_id=pk)
            quantity = product_in.quantity
            if quantity < balance:
                quantity += 1 
                product_in.quantity = quantity
                product_in.save()
            context = {'quantity': quantity}
            return redirect('index')
        else:
            context = {'quantity': 'товара в корзине нет'}
            ProductInCart.objects.create(product_id=pk, quantity=1)
            return redirect('index')
    return redirect('index')

def cart(request):
    products = ProductInCart.objects.all()  
    total = 0
    for product in products:
        total += product.product.price * product.quantity
    context = {
        'products': products,
        'total': total
    }
    return render(request, 'cart.html', context=context)

class ProductDelInCart(DeleteView):
    template_name = 'cart.html'
    model = ProductInCart
    success_url = reverse_lazy('cart')
    confirm_deletion = False


def del_cart_view(request, pk):
    product = get_object_or_404(ProductInCart, pk=pk)
    product.delete()
    return redirect('cart')

class ProductDelConfirmView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Product
    success_url = reverse_lazy('index')
    


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

            