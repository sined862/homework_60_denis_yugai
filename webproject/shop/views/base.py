from django.shortcuts import render
from shop.models import Product, CategoryChoices
from shop.forms import SearchForm


def index_view(request):
    form = SearchForm()
    choices = CategoryChoices.choices
    if request.method == 'GET':
        if not request.GET.get('title'):
            products = Product.objects.filter(balance__gte = 1).order_by('category', 'title')
            context = {
                'products': products,
                'form': form,
                'choices': choices
            }
            return render(request, 'index.html', context)
        products = Product.objects.filter(title=request.GET.get('title'), balance__gte = 1)
        error = 'Ни одной записи не найдено'
        context = {
            'products': products,
            'form': form,
            'error': error
        }
        return render(request, 'index.html', context)
