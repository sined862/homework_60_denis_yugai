from django.shortcuts import render
from shop.models import Product, CategoryChoices
from shop.forms import SearchForm
from django.views.generic import ListView
from django.db.models import Q
from urllib.parse import urlencode


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    queryset = Product.objects.filter(balance__gte = 1)
    extra_context = {'choices': CategoryChoices.choices}
    context_object_name = 'products'
    ordering = ('category', 'title')
    paginate_by = 4
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context
    


# def index_view(request):
#     form = SearchForm()
#     choices = CategoryChoices.choices
#     if request.method == 'GET':
#         if not request.GET.get('title'):
#             products = Product.objects.filter(balance__gte = 1).order_by('category', 'title')
#             context = {
#                 'products': products,
#                 'form': form,
#                 'choices': choices
#             }
#             return render(request, 'index.html', context)
#         products = Product.objects.filter(title=request.GET.get('title'), balance__gte = 1)
#         error = 'Ни одной записи не найдено'
#         context = {
#             'products': products,
#             'form': form,
#             'error': error
#         }
#         return render(request, 'index.html', context)
