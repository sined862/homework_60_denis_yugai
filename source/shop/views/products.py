from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product, CategoryChoices, ProductInCart, Order, ProductsOrder
from shop.forms import ProductForm, SearchForm, OrderForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.db.models import Sum



class ProductView(DetailView):
    template_name = 'product.html'
    model = Product
    extra_context = {'choices': CategoryChoices.choices}

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        count = ProductInCart.objects.aggregate(sum=Sum('quantity'))
        context['count'] = count
        return context


class ProductAddView(CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm
    extra_context = {'choices': CategoryChoices.choices}

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        count = ProductInCart.objects.aggregate(sum=Sum('quantity')) 
        context['count'] = count
        return context


class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm
    extra_context = {'choices': CategoryChoices.choices}

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        count = ProductInCart.objects.aggregate(sum=Sum('quantity')) 
        context['count'] = count
        return context


class ProductDelView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Product

    def get_success_url(self):
        return reverse('product_del', kwargs={'pk': self.object.pk})


class ProductAddToCart(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        balance = product.balance
        if balance > 0:
            if ProductInCart.objects.filter(product_id=kwargs['pk']).exists():
                product_in_cart = get_object_or_404(ProductInCart, product_id=kwargs['pk'])
                quantity = product_in_cart.quantity
                if quantity < balance:
                    quantity += 1
                    product_in_cart.quantity = quantity
                    product_in_cart.save()
                    return redirect('index')
                return redirect('index')
            else:
                ProductInCart.objects.create(product_id=kwargs['pk'], quantity=1)
                return redirect('index')
        return redirect('index')


class CreateOrderView(View):
    def total_price(self):
        products = ProductInCart.objects.all()
        total = 0
        for product in products:
            total += product.product.price * product.quantity 
        return total

    def get(self, request, *args, **kwargs):
        products = ProductInCart.objects.all()
        form = OrderForm()
        context = {
            'form': form,
            'products': products,
            'total': self.total_price()
            }
        return render(request, 'cart.html', context=context)

    def post(self, request, *args, **kwargs):
        products = ProductInCart.objects.all()
        form = OrderForm(request.POST)
        if not form.is_valid():
            return render(request, 'cart.html', context = {
            'form': form,
            'products': products,
            'total': self.total_price()
            })
        order = Order.objects.create(**form.cleaned_data)
        order_id = Order.objects.last().id
        print(order_id)
        for item in products:
            ProductsOrder.objects.create(quantity=item.quantity, order_id=order_id, product_id=item.product.id)
            product = get_object_or_404(Product, pk=item.product_id)
            product.balance -= item.quantity
            product.save()
        products.delete()
        return redirect('index')

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

            