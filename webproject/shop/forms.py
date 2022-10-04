from django import forms
from django.forms import widgets
from shop.models import CategoryChoices


class SearchForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required = True,
        widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'search', 'placeholder': 'поиск'})
    )


class ProductForm(forms.Form):
    title = forms.CharField(
        max_length = 100,
        required = True,
        label = 'Наименование',
        widget=widgets.TextInput(attrs={'class': 'form-control'})    
    )
    description = forms.CharField(
        max_length = 2000,
        required = True,
        label='Описание',
        widget = widgets.Textarea(attrs={'class': 'form-control', 'style': 'height:150px'})
    )
    photo = forms.CharField(
        max_length=150,
        required=True,
        label='Путь до картинки',
        widget=widgets.TextInput(attrs={'class': 'form-control'})    
    )
    category = forms.ChoiceField(
        choices=CategoryChoices.choices,
        required=False,
        widget=forms.RadioSelect,
        label='Категория'
    )
    balance = forms.IntegerField(
        min_value=0,
        label='Остаток на складе',
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control'})  
    )
    price = forms.DecimalField(
        min_value=0,
        label='Цена',
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control'}) 
    )
