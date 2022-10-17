from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product, CategoryChoices
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

            